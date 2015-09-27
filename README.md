# GlassIdentification
author: cuongnb14

##1. Mô tả bộ dữ liệu
- Số lượng bộ dữ liệu: 214
- Số lượng thuộc tính: 10 (bao gồm thuộc tính id), cộng với thuộc tính phân lớp, tất cả các thuộc tính đều có giá trị liên tục 
- Thông tin thuộc tính: (Đơn vị đo thuộc tính 3 đến 10 là phần trăm trọng lượng trong oxit tương ứng ).
  - (1) ID: 1 -> 214
  - (2) RI: Chỉ số khúc xạ
  - (3) Na: Sodium
  - (4) Mg: Magnesium
  - (5) Al: Aluminum
  - (6) Si: Silicon
  - (7) K: Potassium
  - (8) Ca: Calcium
  - (9) Ba: Barium
  - (10) Fe: Iron
  - (11) Loại kính: nhận 1 trong các giá trị sau:
    - 1 building_windows_float_processed
    - 2 building_windows_non_float_processed
    - 3 vehicle_windows_float_processed
    - 4 vehicle_windows_non_float_processed (none in this database)
    - 5 containers
    - 6 tableware
    - 7 headlamps
- Không có giá trị thuộc tính nào bị thiếu. 

##2. Mờ hóa
Chú ý (bỏ thuộc tính id)
- Với mỗi thuộc tính mờ hóa thành 2 lớp (với min,max là giá trị nhỏ nhất, lớn nhất của thuộc tính trong bộ dữ liệu):
  - Low: là tập mờ tam giác (min,min,max)
  - Height: là tập mờ tam giác (min,max,max)
- Với một bộ dữ liệu. Mỗi thuộc tính Xi chọn tập mờ Ai (Ai là Lowi hoặc Heighti), sao cho uA của Xi là lớn nhất, thì sinh đưọc một luật:
  - N X1 là A1 ... và X9 là A9 thì Y là Bj với độ thuộc là giá trị nhỏ nhất của các độ thuộc uAi(Xi)
- Loại bỏ luật có độ thuộ dứoi ngưỡng 0.5
- Loại bỏ các luật có chung vế trái, chỉ giữ lại luật có độ thuộc lớn nhất
