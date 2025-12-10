-- ============ داده‌های اضافی برای آزمایش ============

USE IT_Asset_Management;
GO

-- داده‌های نمونه بیشتر برای دارایی‌ها
INSERT INTO assets (asset_number, name, description, category_id, asset_type, status, purchase_date, purchase_price, owner_id, department_id, location_id, serial_number, model, manufacturer) VALUES
(N'ASSET-005', N'سرور وب', N'سرور وب شرکت', 2, N'Virtual Server', N'فعال', '2023-01-10', 10000, 2, 1, 1, N'VM-SN555666', N'VM Web Server', N'Virtual'),
(N'ASSET-006', N'لپ‌تاپ HR', N'لپ‌تاپ بخش HR', 6, N'Laptop', N'فعال', '2023-06-15', 12000, 3, 2, 4, N'LP-SN777888', N'ThinkPad E14', N'Lenovo'),
(N'ASSET-007', N'لپ‌تاپ مالی', N'لپ‌تاپ بخش مالی', 6, N'Laptop', N'فعال', '2023-07-20', 12000, 4, 3, 4, N'LP-SN999000', N'ThinkPad E14', N'Lenovo'),
(N'ASSET-008', N'پرینتر - طبقه 2', N'پرینتر Color', 8, N'Printer', N'فعال', '2022-12-01', 5000, NULL, 1, 3, N'PR-SN111222', N'LaserJet Pro', N'HP'),
(N'ASSET-009', N'سوئیچ شبکه', N'سوئیچ 48 پورت', 9, N'Network Switch', N'فعال', '2022-03-10', 20000, 2, 1, 1, N'SW-SN333444', N'Catalyst 2960', N'Cisco'),
(N'ASSET-010', N'روتر اصلی', N'روتر اصلی شرکت', 10, N'Router', N'فعال', '2022-04-15', 8000, 2, 1, 1, N'ROU-SN555666', N'ISR 4451', N'Cisco'),
(N'ASSET-011', N'UPS اصلی', N'منبع تغذیه بدون قطع', 11, N'UPS', N'فعال', '2021-10-20', 25000, 2, 1, 1, N'UPS-SN777888', N'Symmetra PX 20kVA', N'Eaton');

-- تاریخچه اضافی
INSERT INTO asset_histories (asset_id, user_id, change_type, old_value, new_value, description) VALUES
(2, 2, N'ایجاد دارایی', N'', N'فایروال Palo Alto', N'فایروال جدید نصب شد'),
(5, 2, N'ایجاد دارایی', N'', N'سرور وب', N'سرور وب ایجاد شد'),
(8, 2, N'ایجاد دارایی', N'', N'پرینتر Color', N'پرینتر جدید نصب شد'),
(6, 3, N'نقل مکان', N'دفتر مدیریت - طبقه 3', N'دفتر HR - طبقه 1', N'نقل مکان انجام شد');

GO

PRINT N'داده‌های اضافی درج شد!';
