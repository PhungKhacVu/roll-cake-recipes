# Cơ sở dữ liệu công thức bánh bông lan cuộn

Cơ sở dữ liệu này chứa các công thức làm bánh bông lan cuộn được thu thập và phân tích theo xu hướng thị trường. Mục đích là cung cấp một nguồn tài nguyên phong phú cho việc nghiên cứu, phát triển sản phẩm và chia sẻ công thức với khách hàng.

## Cấu trúc dữ liệu

Cơ sở dữ liệu được lưu trữ dưới dạng file CSV (`roll_cake_recipes.csv`) với các trường dữ liệu sau:

*   **Recipe_ID**: Mã định danh duy nhất cho mỗi công thức.
*   **Recipe_Name**: Tên của công thức.
*   **Description**: Mô tả ngắn gọn về công thức.
*   **Category**: Phân loại công thức (ví dụ: Hiện đại, Truyền thống).
*   **Flavor_Profile**: Hồ sơ hương vị chính của bánh (ví dụ: Chocolate, Trái cây, Trà xanh).
*   **Difficulty_Level**: Mức độ khó của công thức (ví dụ: Dễ, Trung bình, Khó).
*   **Prep_Time_Minutes**: Thời gian chuẩn bị tính bằng phút.
*   **Cook_Time_Minutes**: Thời gian nấu/nướng tính bằng phút.
*   **Total_Time_Minutes**: Tổng thời gian cần thiết tính bằng phút.
*   **Servings**: Số lượng khẩu phần ăn mà công thức tạo ra.
*   **Image_URL**: Đường dẫn URL đến hình ảnh của bánh.
*   **Video_URL**: Đường dẫn URL đến video hướng dẫn (nếu có).
*   **Source**: Nguồn gốc của công thức.
*   **Date_Created**: Ngày công thức được tạo hoặc xuất bản.
*   **Date_Updated**: Ngày công thức được cập nhật lần cuối.
*   **Ingredients_Flattened**: Danh sách các thành phần được làm phẳng thành một chuỗi, bao gồm tên, số lượng, đơn vị và ghi chú.
*   **Instructions_Flattened**: Danh sách các bước hướng dẫn được làm phẳng thành một chuỗi, mỗi bước trên một dòng mới.
*   **Tips_Tricks**: Các mẹo và thủ thuật hữu ích cho công thức.
*   **Storage_Instructions**: Hướng dẫn bảo quản bánh.
*   **Customer_Feedback_Score**: Điểm đánh giá từ khách hàng (nếu có).
*   **Market_Trend_Relevance**: Mức độ liên quan đến xu hướng thị trường (ví dụ: Cao, Trung bình, Thấp).

## Hướng dẫn sử dụng

1.  **Tải xuống:** Tải file `roll_cake_recipes.csv` về máy tính của bạn.
2.  **Mở bằng phần mềm bảng tính:** Bạn có thể mở file CSV bằng các phần mềm như Microsoft Excel, Google Sheets, LibreOffice Calc hoặc bất kỳ trình soạn thảo văn bản nào.
3.  **Phân tích dữ liệu:** Sử dụng các công cụ phân tích dữ liệu trong phần mềm bảng tính để lọc, sắp xếp và tạo biểu đồ từ dữ liệu. Ví dụ, bạn có thể phân tích các hương vị phổ biến, độ khó trung bình, hoặc các thành phần được sử dụng nhiều nhất.
4.  **Cập nhật:** Để cập nhật cơ sở dữ liệu, bạn có thể chỉnh sửa trực tiếp file CSV hoặc thêm các công thức mới theo cấu trúc đã định.
5.  **Nghiên cứu và chia sẻ:** Sử dụng thông tin từ cơ sở dữ liệu để nghiên cứu xu hướng, tạo ra các công thức mới hoặc gửi các công thức đã chọn đến khách hàng của bạn.

## Phân tích dữ liệu

Các biểu đồ phân tích dữ liệu đã được tạo ra và lưu dưới dạng hình ảnh:

*   `flavor_analysis.png`: Biểu đồ phân tích hương vị bánh bông lan cuộn.
*   `difficulty_analysis.png`: Biểu đồ phân tích độ khó của các công thức.
*   `ingredient_analysis.png`: Biểu đồ các thành phần phổ biến nhất.

Các biểu đồ này cung cấp cái nhìn tổng quan về các đặc điểm chính của các công thức trong cơ sở dữ liệu.

