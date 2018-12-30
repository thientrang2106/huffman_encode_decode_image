=== Hướng dẫn sử dụng chương trình nén ảnh===
1. Yêu cầu phần mềm, thư viện
- Cần sử dụng python > 3. Đây là hướng dẫn cài đặt python https://o7planning.org/vi/11375/huong-dan-cai-dat-va-cau-hinh-python
- Cần cài đặt sẵn các thư viện của python sau:
	+ PyQt5 - Thư viện dùng để tạo giao diện: pip install pyqt5 
	+ numpy - Thư viện hỗ trợ lưu trử xử lý trên mảng: pip install numpy
	+ PIL - Thư việc hỗ trợ xử lý việc đọc, lưu, mở,... ảnh: pip install pillow
	+ huffman - Thư viện thuật toán huffman để giúp cho nén chuẩn JPEG: pip install huffman
	+opencv - Thư viện hỗ trợ xử lý ảnh: pip install opencv-python

2. Hướng dẫn sử dụng chương trình
Chương trình bao gồm:
- gd.py: Chứa code để chạy giao diện và đã kết nối với các chương trình của thuật toán còn lại,
- huffman.py: Chứa code của thuật toán nén ảnh huffman,
- lzw.py: Chứa code của thuật toán nén ảnh lzw,

Hướng dẫn sử dụng:
- Dùng bất cứ IDE nào hỗ trợ chạy python.
- Chạy chương trình gd.py. Sau đó sẽ xuất hiện giao diện chương trình.
- Tiếp theo chỉ cần nhấn chọn file cần nén/giải nén (Lưu ý đối với file nén phải là file ảnh, còn file giải nén phải là file .bin),
- Sau đó, chọn thuật toán (Lưu ý khi chọn thuật toán để giải nén cần khớp với file nén),
- Cuối cùng nhấn nút nén/giải nén.

Chân thành cảm ơn!