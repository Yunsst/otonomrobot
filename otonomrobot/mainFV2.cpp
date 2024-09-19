#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/imgcodecs/imgcodecs.hpp>
#include <opencv2/dnn.hpp>
#include <iostream>
#include <stdio.h>
#include <vector>
#include <string>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <unordered_map>
#include <chrono>
#include "yolo-fastestv2.h"

yoloFastestv2 yoloF2;

const char* class_names[] = {
    "background", "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck",
    "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird",
    "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
    "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "sofa", "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator",
    "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
};

// Yap?lar? ve zamanlar? izlemek için bir yap? tan?mlayal?m
struct TrackedObject {
    std::chrono::steady_clock::time_point last_seen;
    bool saved;
};

std::unordered_map<std::string, TrackedObject> detected_objects;

std::string get_box_id(const TargetBox& box) {
    return std::string(class_names[box.cate + 1]) + "_" + std::to_string(box.x1) + "_" + std::to_string(box.y1) + "_" + std::to_string(box.x2) + "_" + std::to_string(box.y2);
}

void non_max_suppression(const std::vector<TargetBox>& boxes, std::vector<TargetBox>& nms_boxes, float score_threshold, float iou_threshold) {
    std::vector<int> indices;
    std::vector<cv::Rect> rects;
    std::vector<float> scores;

    for (const auto& box : boxes) {
        if (box.score >= score_threshold) {
            rects.push_back(cv::Rect(box.x1, box.y1, box.x2 - box.x1, box.y2 - box.y1));
            scores.push_back(box.score);
        }
    }

    cv::dnn::NMSBoxes(rects, scores, score_threshold, iou_threshold, indices);

    for (int idx : indices) {
        nms_boxes.push_back(boxes[idx]);
    }
}

static void draw_objects(cv::Mat& cvImg, const std::vector<TargetBox>& boxes, int new_socket)
{
    std::string data_to_send;
    auto now = std::chrono::steady_clock::now();
    bool new_detection = false;

    int bottom_line_y = cvImg.rows - 1;
    int upper_line_y = cvImg.rows - 101;

    bool object_in_roi = false;

    for (size_t i = 0; i < boxes.size(); i++) {
        std::cout << "Box " << i << ": "
                  << "x1=" << boxes[i].x1 << " y1=" << boxes[i].y1
                  << " x2=" << boxes[i].x2 << " y2=" << boxes[i].y2
                  << " score=" << boxes[i].score << " category=" << class_names[boxes[i].cate + 1]
                  << std::endl;

        char text[256];
        sprintf(text, "%s %.1f%% (x1=%d, y1=%d, x2=%d, y2=%d)",
                class_names[boxes[i].cate + 1], boxes[i].score * 100,
                boxes[i].x1, boxes[i].y1, boxes[i].x2, boxes[i].y2);

        int baseLine = 0;
        cv::Size label_size = cv::getTextSize(text, cv::FONT_HERSHEY_SIMPLEX, 0.5, 1, &baseLine);

        int x = boxes[i].x1;
        int y = boxes[i].y1 - label_size.height - baseLine;
        if (y < 0) y = 0;
        if (x + label_size.width > cvImg.cols) x = cvImg.cols - label_size.width;

        cv::rectangle(cvImg, cv::Rect(cv::Point(x, y), cv::Size(label_size.width, label_size.height + baseLine)),
                      cv::Scalar(255, 255, 255), -1);

        cv::putText(cvImg, text, cv::Point(x, y + label_size.height),
                    cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 0, 0));

        cv::rectangle(cvImg, cv::Point(boxes[i].x1, boxes[i].y1),
                      cv::Point(boxes[i].x2, boxes[i].y2), cv::Scalar(255, 0, 0));

        data_to_send += std::string(text) + "\n";

        std::string box_id = get_box_id(boxes[i]);
        if (detected_objects.find(box_id) == detected_objects.end()) {
            detected_objects[box_id] = {now, false};
            new_detection = true; // Yeni bir nesne alg?land?
            if (class_names[boxes[i].cate + 1]=="laptop") {
                    cv::imwrite("output.png", cvImg);
                    send(new_socket, data_to_send.c_str(), data_to_send.size(), 0);
                }

        } else {
            detected_objects[box_id].last_seen = now;
        }

        // E?er bounding box ROI içinde ise object_in_roi flag'ini true yap
        if (boxes[i].y2 >= upper_line_y && boxes[i].y1 <= bottom_line_y) {
            object_in_roi = true;
        }
    }


    // Yeni bir nesne alg?land?ysa veya belirli bir süre boyunca alg?lanmayan bir nesne varsa kaydet
    

    // E?er ROI içinde bir bounding box varsa, "Object Detected" yaz?s?n? ekle
    //if (object_in_roi) {
    //    cv::putText(cvImg, "Object Detected", cv::Point(cvImg.cols / 2 - 100, cvImg.rows / 2),
    //                cv::FONT_HERSHEY_SIMPLEX, 1.0, cv::Scalar(0, 0, 255), 2);


    //}
}

int main(int argc, char** argv)
{
    float f;
    float FPS[16];
    int i, Fcnt = 0;
    cv::Mat frame;
    std::chrono::steady_clock::time_point Tbegin, Tend;

    for (i = 0; i < 16; i++) FPS[i] = 0.0;

    yoloF2.init(false); //we have no GPU

    yoloF2.loadModel("yolo-fastestv2-opt.param", "yolo-fastestv2-opt.bin");

    cv::VideoCapture cap(0);
    if (!cap.isOpened()) {
        std::cerr << "ERROR: Unable to open the camera" << std::endl;
        return 0;
    }

    std::cout << "Start grabbing, press ESC on Live window to terminate" << std::endl;

    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(8080);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
        perror("accept");
        exit(EXIT_FAILURE);
    }

    while (1) {
        cap >> frame;
        if (frame.empty()) {
            std::cerr << "ERROR: Unable to grab from the camera" << std::endl;
            break;
        }

        Tbegin = std::chrono::steady_clock::now();

        std::vector<TargetBox> boxes;
        yoloF2.detection(frame, boxes);

        // Non-Maximum Suppression (NMS) ve belirli bir e?ik de?eri kullanarak sonuçlar? filtrele
        std::vector<TargetBox> nms_boxes;
        float score_threshold = 0.5;
        float iou_threshold = 0.4;
        non_max_suppression(boxes, nms_boxes, score_threshold, iou_threshold);

        // ROI çizgilerini ekle
        int bottom_line_y = frame.rows - 1;
        int upper_line_y = frame.rows - 151;

        //cv::line(frame, cv::Point(0, bottom_line_y), cv::Point(frame.cols, bottom_line_y), cv::Scalar(0, 255, 0), 2);
        //cv::line(frame, cv::Point(0, upper_line_y), cv::Point(frame.cols, upper_line_y), cv::Scalar(0, 255, 0), 2);

        draw_objects(frame, nms_boxes, new_socket);

        Tend = std::chrono::steady_clock::now();

        f = std::chrono::duration_cast<std::chrono::milliseconds>(Tend - Tbegin).count();
        if (f > 0.0) FPS[((Fcnt++) & 0x0F)] = 1000.0 / f;
        for (f = 0.0, i = 0; i < 16; i++) { f += FPS[i]; }
        putText(frame, cv::format("FPS %0.2f", f / 16), cv::Point(10, 20), cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0, 0, 255));

        cv::imshow("Raspberry Pi 5", frame);
        char esc = cv::waitKey(5);
        if (esc == 27) break;
    }

    close(new_socket);
    close(server_fd);
    return 0;
}
