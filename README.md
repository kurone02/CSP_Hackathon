# CSP_Hackathon
 Server cho Hackathon

## Cài đặt
 Chỉ cần download là xong
 
## Thiết lập kỳ thi
 - Chỉnh sửa file **contest.json** trong thư mục **Hackathon** trước khi chạy server
 ```json
 {
    "timestart": "Thời_gian_bắt_đầu",
    "duration": "Thời gian làm bài",
    "problem": [
        {
            "problem_id": "<ID của bài (Không được trùng lặp)>",
            "problem_name": "<Tên bài>",
            "nSubtasks": "Số lượng subtask",
            "subtask_<số thứ tự>": "<đáp án>",
            "Checker_<số thứ tự>": <1 trong 3 checker sau: "integer", "real", "string">,
            "subtask_<số thứ tự>": "<đáp án>",
            "Checker_<số thứ tự>": <1 trong 3 checker sau: "integer", "real", "string">,
            "subtask_<số thứ tự>": "<đáp án>",
            "Checker_<số thứ tự>": <1 trong 3 checker sau: "integer", "real", "string">,
            "subtask_<số thứ tự>": "<đáp án>",
            "Checker_<số thứ tự>": <1 trong 3 checker sau: "integer", "real", "string">
        },
        {
            "problem_id": "B",
            "problem_name": "Clock",
            "nSubtasks": "1",
            "subtask_1": "1",
            "Checker_1": "integer"
        },
    ]
}
 ```
 
## Chạy server
 chạy file run_server.bat
 
