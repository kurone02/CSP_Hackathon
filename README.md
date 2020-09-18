# CSP_Hackathon
 Server cho Hackathon

## Cài đặt
 Chỉ cần download là xong
 
## Thiết lập kỳ thi
 - Chỉnh sửa file **contest.json** trong thư mục **Hackathon** trước khi chạy server
 ```json
 {
    "timestart": <Thời gian bắt đầu>,
    "duration": <Thời gian làm bài>,
    "problem": [
        {
            "problem_id": "<ID của bài (Không được trùng lặp)>",
            "problem_name": "<Tên bài>",
            "nSubtasks": <Số lượng subtask>,
            "subtask_<số thứ tự>": "<đáp án>",
            "subtask_<số thứ tự>": "<đáp án>",
            "subtask_<số thứ tự>": "<đáp án>",
            "subtask_<số thứ tự>": "<đáp án>"
            ...
        },
        {
            "problem_id": "B",
            "problem_name": "Clock",
            "nSubtasks": "1",
            "subtask_1": "1"
        },
        ...
    ]
}
 ```
 
## Chạy server
 ```bash
 python run.py
 ```
 
