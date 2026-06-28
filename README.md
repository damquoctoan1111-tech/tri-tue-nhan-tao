# 🚀 Hệ Thống Giải Mã 8-Puzzle Toàn Diện – Tích Hợp 6 Nhóm Thuật Toán AI

Đồ án môn **Trí tuệ nhân tạo** tập trung nghiên cứu, tối ưu hóa và mô phỏng trực quan hóa lời giải bài toán **8-Puzzle**. Hệ thống sở hữu kiến trúc mã nguồn mô-đun hóa độc lập và tường minh, triển khai đầy đủ cả 6 nhóm giải thuật lý thuyết cốt lõi từ cơ bản đến nâng cao.

---

## 1. Mục Tiêu Đồ Án

- **Trực quan hóa thuật toán:** Chuyển đổi các bước xử lý trừu tượng trên không gian trạng thái thành các dịch chuyển ô cờ trực quan trên màn hình.
- **Thực nghiệm & Đối sánh:** Cung cấp nền tảng đo lường hiệu năng thời gian thực để phân tích, so sánh ưu-nhược điểm của từng nhóm tiếp cận AI.
- **Kiến trúc mã nguồn sạch:** Tổ chức hệ thống module tách biệt, không phụ thuộc thư viện bắc cầu, giúp đơn giản hóa quá trình debug, kiểm tra và đánh giá học thuật.

---

## 2. Bản Đồ Thuật Toán Đã Triển Khai

Hệ thống được cấu trúc hóa thành 6 phân hệ thuật toán chạy độc lập:

### 🔹 Tìm Kiếm Mù (Uninformed Search)
- **BFS (Breadth-First Search):** Tìm kiếm theo chiều rộng.
- **DFS (Depth-First Search):** Tìm kiếm theo chiều sâu.
- **UCS (Uniform Cost Search):** Tìm kiếm giá trị đồng nhất.
- **IDS (Iterative Deepening Search):** Tìm kiếm sâu dần.

### 🔹 Tìm Kiếm Có Tri Thức (Informed Search)
- **GBFS (Greedy Best-First Search):** Tìm kiếm tham lam theo hàm ý.
- **A\* Search:** Thuật toán tìm kiếm tối ưu kết hợp chi phí thực tế và heuristic.
- **IDA\* (Iterative Deepening A\*):** Thuật toán A\* sâu dần tối ưu bộ nhớ.

### 🔹 Tìm Kiếm Cục Bộ (Local Search)
- **Simple Hill Climbing:** Leo đồi cơ bản.
- **Stochastic Hill Climbing:** Leo đồi ngẫu nhiên.
- **Random Restart Hill Climbing:** Leo đồi khởi tạo lại ngẫu nhiên để vượt điểm cực đại cục bộ.
- **Local Beam Search:** Tìm kiếm chùm tia cục bộ.
- **Simulated Annealing:** Thuật toán luyện kim (Mô phỏng ủ thép).

### 🔹 Tìm Kiếm Trong Môi Trường Phức Tạp (Complex Environments)
- **Belief State Search (No observation):** Tìm kiếm trạng thái tin tưởng không có quan sát.
- **Belief State Search (Partial observation):** Tìm kiếm trạng thái tin tưởng có quan sát một phần.
- **AND-OR Graph Search:** Tìm kiếm trên đồ thị VÀ-HOẶC.

### 🔹 Bài Toán Thỏa Mãn Ràng Buộc (CSP)
- **Backtracking Search:** Tìm kiếm quay lui hệ thống.
- **Forward Checking:** Kiểm tra lan truyền ràng buộc trước.
- **AC-3 Search:** Thuật toán duy trì tính nhất quán của cung (Arc Consistency).
- **Min-Conflicts:** Thuật toán giảm thiểu xung đột cục bộ.

### 🔹 Tìm Kiếm Đối Kháng (Adversarial Search)
- **Minimax:** Cây quyết định trò chơi hai tác tử.
- **Alpha-Beta Pruning:** Kỹ thuật cắt tỉa Alpha-Beta tăng tốc cây quyết định.
- **Expectimax:** Mô phỏng nước đi tối ưu trong môi trường có yếu tố xác suất ngẫu nhiên.

> ⚠️ **Lưu ý học thuật:** Trò chơi 8-Puzzle bản chất là bài toán một tác tử (Single-agent). Các phân hệ thuộc nhóm CSP và Adversarial Search được cấu hình dưới dạng giả lập/mở rộng logic nhằm phục vụ cho mục đích minh họa thuật toán trực quan theo yêu cầu nghiên cứu của môn học.

---


## 3. Chức Năng Chính

- **Cấu hình trạng thái linh hoạt:** Hỗ trợ nhập tay thủ công cấu hình ma trận khởi đầu/đích hoặc tự động sinh ngẫu nhiên một trạng thái bàn cờ hợp lệ (đảm bảo giải được thông qua kiểm tra số lượng nghịch thế).
- **Lựa chọn Heuristic đa dạng:** Dễ dàng chuyển đổi trực tiếp giữa hàm đếm số ô sai vị trí (Misplaced Tiles) và tính tổng khoảng cách Manhattan.
- **Trình điều khiển mô phỏng trực quan:** Tích hợp bộ thanh trượt chỉnh tốc độ, tự động chạy (Play), tạm dừng (Pause), dịch chuyển từng bước cờ (Next/Previous step) hoặc chuyển nhanh về trạng thái đầu/cuối.
- **Đo lường thông số chuyên sâu:** Hiển thị thời gian thực các thông số hiệu năng chuyên nghiệp bao gồm: Độ dài lời giải (Cost), số lượng nút đã mở rộng (Expanded Nodes), số nút được sinh ra (Generated Nodes), kích thước biên lưu trữ lớn nhất (Max Frontier), và tổng thời gian tính toán chính xác đến từng micro giây.
- **Quản lý nhật ký thông minh:** Tự động lưu lịch sử chạy vào file JSON và kết xuất lên bảng hiển thị giao diện có thanh cuộn đa hướng, giúp người dùng so sánh dữ liệu trực quan mà không lo bị che khuất thông tin.

---

## 4. Cách Chạy Chương Trình

Yêu cầu máy tính cài đặt **Python từ phiên bản 3.10 trở lên**.

Kích hoạt môi trường và khởi chạy giao diện ứng dụng bằng cách thực hiện một trong hai lệnh sau tại cửa sổ dòng lệnh (Terminal) của dự án:
```bash
python main.py

##6. Cách Commit Lên GitHub
git init
git add .
git commit -m "Initial commit: Hoàn thiện cấu trúc độc lập cho 6 nhóm thuật toán AI bài toán 8-Puzzle"
git branch -M main
git remote add origin https://github.com/damquoctoan1111-tech/tri-tue-nhan-tao.git
git push -u origin main --force

##7. Sinh viên thực hiện
- Đàm Quốc Toàn
- mssv: 24110355
