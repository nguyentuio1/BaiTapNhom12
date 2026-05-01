# BaiTapNhom12 — Ứng dụng Đồ thị

Ứng dụng đồ thị viết bằng Python cho môn Lý thuyết đồ thị.

## Cài đặt

```bash
pip install -r requirements.txt
```

## Chạy

```bash
python main.py
```

## Chức năng

### Cơ bản
1. Vẽ đồ thị trực quan — click trên canvas để thêm đỉnh, click 2 đỉnh khác nhau để nối cạnh, kéo thả để di chuyển, chuột phải để xóa đỉnh
2. Lưu/đọc đồ thị (`.json` hoặc `.txt` ma trận kề)
3. Tìm đường đi ngắn nhất (Dijkstra cho đồ thị có trọng số, BFS cho không trọng số)
4. Duyệt BFS, DFS có animation
5. Kiểm tra đồ thị 2 phía
6. Chuyển đổi 3 biểu diễn: ma trận kề ↔ danh sách kề ↔ danh sách cạnh (cả vô hướng & có hướng)

### Nâng cao (animation từng bước)
- Prim — cây khung nhỏ nhất từ một đỉnh
- Kruskal — cây khung nhỏ nhất bằng sắp xếp cạnh
- Ford-Fulkerson — luồng cực đại
- Fleury — đường đi/chu trình Euler
- Hierholzer — chu trình Euler bằng stack

## Cách dùng

1. Bấm **Mới** → chọn có hướng / có trọng số
2. Click trên canvas để thêm đỉnh (tự đặt tên A, B, C, …)
3. Click vào 2 đỉnh khác nhau để nối cạnh (nếu có trọng số sẽ hỏi giá trị)
4. Chọn đỉnh **Nguồn** và **Đích**
5. Bấm tên thuật toán → xem animation
6. Dùng thanh điều khiển ◀ ▶ play/pause, kéo slider chỉnh tốc độ

## Đồ thị mẫu

Trong thư mục `samples/`, mở bằng nút **Mở**:
- `dothi_co_trong_so.json` — đồ thị vô hướng có trọng số
- `dothi_2_phia.json` — đồ thị 2 phía
- `dothi_euler.json` — đồ thị có chu trình Euler (cho Fleury, Hierholzer)
- `dothi_luong.json` — đồ thị có hướng cho Ford-Fulkerson
