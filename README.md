# CSP_Hackathon
 Server cho Hackathon

## Cài đặt
 - Cài python tại: https://www.python.org/downloads/
 - Cài pip tại: https://pip.pypa.io/en/stable/installing/
 - Bật cmd, chạy: 
 ```bash
    pip install -r requirements.txt
 ```
 
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
            "checker_<số thứ tự>": "<1 trong 3 checker sau: "integer", "real", "string">",
            "score_<số thứ tự>": "<Số điểm của subtask>",
            "subtask_<số thứ tự>": "<đáp án>",
            "checker_<số thứ tự>": "<1 trong 3 checker sau: "integer", "real", "string">",
            "score_<số thứ tự>": "<Số điểm của subtask>",
            "subtask_<số thứ tự>": "<đáp án>",
            "checker_<số thứ tự>": "<1 trong 3 checker sau: "integer", "real", "string">",
            "score_<số thứ tự>": "<Số điểm của subtask>",
            "subtask_<số thứ tự>": "<đáp án>",
            "checker_<số thứ tự>": "<1 trong 3 checker sau: "integer", "real", "string">",
            "score_<số thứ tự>": "<Số điểm của subtask>"
        },
        {
            "problem_id": "B",
            "problem_name": "Clock",
            "nSubtasks": "1",
            "subtask_1": "1",
            "checker_1": "integer"
            "score_1": 100,
        },
    ]
}
 ```
 
## Chạy server
 - Chạy 
 ```bash
    python main.py
 ```
 
