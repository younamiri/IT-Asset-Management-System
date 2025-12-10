-- ============ ایجاد پایگاه‌داده ============

USE master;
GO

IF EXISTS (SELECT * FROM sys.databases WHERE name = 'IT_Asset_Management')
BEGIN
    ALTER DATABASE IT_Asset_Management SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE IT_Asset_Management;
END
GO

CREATE DATABASE IT_Asset_Management;
GO

USE IT_Asset_Management;
GO

-- ============ جدول departments (واحدهای سازمانی) ============

CREATE TABLE departments (
    id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(100) NOT NULL UNIQUE,
    code NVARCHAR(20) NOT NULL UNIQUE,
    description NVARCHAR(MAX),
    parent_id INT,
    created_at DATETIME DEFAULT GETUTCDATE(),
    updated_at DATETIME DEFAULT GETUTCDATE(),
    FOREIGN KEY (parent_id) REFERENCES departments(id)
);

CREATE INDEX idx_departments_code ON departments(code);
CREATE INDEX idx_departments_parent_id ON departments(parent_id);

-- ============ جدول users (کاربران) ============

CREATE TABLE users (
    id INT PRIMARY KEY IDENTITY(1,1),
    username NVARCHAR(50) NOT NULL UNIQUE,
    email NVARCHAR(100) NOT NULL UNIQUE,
    full_name NVARCHAR(100) NOT NULL,
    department_id INT,
    is_admin BIT DEFAULT 0,
    is_active BIT DEFAULT 1,
    ad_user_id NVARCHAR(100),
    created_at DATETIME DEFAULT GETUTCDATE(),
    updated_at DATETIME DEFAULT GETUTCDATE(),
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_department_id ON users(department_id);

-- ============ جدول asset_categories (دسته‌های دارایی) ============

CREATE TABLE asset_categories (
    id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(100) NOT NULL UNIQUE,
    description NVARCHAR(MAX),
    asset_type NVARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT GETUTCDATE(),
    updated_at DATETIME DEFAULT GETUTCDATE()
);

CREATE INDEX idx_asset_categories_name ON asset_categories(name);
CREATE INDEX idx_asset_categories_asset_type ON asset_categories(asset_type);

-- ============ جدول locations (مکان‌های دارایی) ============

CREATE TABLE locations (
    id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(100) NOT NULL UNIQUE,
    building NVARCHAR(50),
    floor INT,
    room NVARCHAR(50),
    description NVARCHAR(MAX),
    created_at DATETIME DEFAULT GETUTCDATE(),
    updated_at DATETIME DEFAULT GETUTCDATE()
);

CREATE INDEX idx_locations_name ON locations(name);
CREATE INDEX idx_locations_building ON locations(building);

-- ============ جدول assets (دارایی‌های فناوری اطلاعات) ============

CREATE TABLE assets (
    id INT PRIMARY KEY IDENTITY(1,1),
    asset_number NVARCHAR(50) NOT NULL UNIQUE,
    name NVARCHAR(100) NOT NULL,
    description NVARCHAR(MAX),
    category_id INT NOT NULL,
    asset_type NVARCHAR(50) NOT NULL,
    status NVARCHAR(20) DEFAULT N'فعال',
    
    -- اطلاعات مالی
    purchase_date DATETIME,
    purchase_price FLOAT,
    depreciation_rate FLOAT DEFAULT 0.0,
    warranty_expiry DATETIME,
    
    -- مالک و مکان
    owner_id INT,
    department_id INT,
    location_id INT,
    
    -- مشخصات فنی
    serial_number NVARCHAR(100) UNIQUE,
    model NVARCHAR(100),
    manufacturer NVARCHAR(100),
    
    -- تاریخچه
    created_at DATETIME DEFAULT GETUTCDATE(),
    updated_at DATETIME DEFAULT GETUTCDATE(),
    
    FOREIGN KEY (category_id) REFERENCES asset_categories(id),
    FOREIGN KEY (owner_id) REFERENCES users(id),
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

CREATE INDEX idx_assets_asset_number ON assets(asset_number);
CREATE INDEX idx_assets_category_id ON assets(category_id);
CREATE INDEX idx_assets_owner_id ON assets(owner_id);
CREATE INDEX idx_assets_department_id ON assets(department_id);
CREATE INDEX idx_assets_location_id ON assets(location_id);
CREATE INDEX idx_assets_status ON assets(status);
CREATE INDEX idx_assets_asset_type ON assets(asset_type);

-- ============ جدول asset_histories (تاریخچه تغییرات) ============

CREATE TABLE asset_histories (
    id INT PRIMARY KEY IDENTITY(1,1),
    asset_id INT NOT NULL,
    user_id INT NOT NULL,
    change_type NVARCHAR(50),
    old_value NVARCHAR(MAX),
    new_value NVARCHAR(MAX),
    description NVARCHAR(MAX),
    created_at DATETIME DEFAULT GETUTCDATE(),
    
    FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_asset_histories_asset_id ON asset_histories(asset_id);
CREATE INDEX idx_asset_histories_user_id ON asset_histories(user_id);
CREATE INDEX idx_asset_histories_created_at ON asset_histories(created_at);

-- ============ جدول reports (گزارش‌ها) ============

CREATE TABLE reports (
    id INT PRIMARY KEY IDENTITY(1,1),
    title NVARCHAR(200) NOT NULL,
    report_type NVARCHAR(50),
    filters NVARCHAR(MAX),
    created_by_id INT,
    created_at DATETIME DEFAULT GETUTCDATE(),
    updated_at DATETIME DEFAULT GETUTCDATE(),
    
    FOREIGN KEY (created_by_id) REFERENCES users(id)
);

CREATE INDEX idx_reports_report_type ON reports(report_type);
CREATE INDEX idx_reports_created_by_id ON reports(created_by_id);

-- ============ داده‌های نمونه ============

-- واحدهای سازمانی
INSERT INTO departments (name, code, description) VALUES
(N'فناوری اطلاعات', N'IT', N'واحد فناوری اطلاعات'),
(N'منابع انسانی', N'HR', N'واحد منابع انسانی'),
(N'مالی و حسابداری', N'FINANCE', N'واحد مالی و حسابداری'),
(N'فروش', N'SALES', N'واحد فروش'),
(N'بازاریابی', N'MARKETING', N'واحد بازاریابی');

-- دسته‌های دارایی
INSERT INTO asset_categories (name, description, asset_type) VALUES
(N'سرورهای فیزیکی', N'سرورهای فیزیکی شرکت', N'Physical Server'),
(N'سرورهای مجازی', N'سرورهای مجازی VMware/Hyper-V', N'Virtual Server'),
(N'فایروال', N'دستگاه‌های فایروال', N'Firewall'),
(N'All In One', N'دستگاه‌های All In One', N'All In One'),
(N'تلفن‌های IP', N'تلفن‌های IP', N'Phone'),
(N'لپ‌تاپ', N'لپ‌تاپ‌های شرکت', N'Laptop'),
(N'کامپیوتر رومیزی', N'کامپیوتر‌های رومیزی', N'Desktop'),
(N'پرینتر', N'دستگاه‌های پرینتر', N'Printer'),
(N'سوئیچ شبکه', N'سوئیچ‌های شبکه', N'Network Switch'),
(N'روتر', N'دستگاه‌های روتر', N'Router'),
(N'UPS', N'منبع تغذیه بدون قطع', N'UPS');

-- مکان‌های دارایی
INSERT INTO locations (name, building, floor, room, description) VALUES
(N'اتاق سرور - ساختمان A', N'A', 1, N'SR-001', N'اتاق سرور اصلی'),
(N'اتاق سرور - ساختمان B', N'B', 0, N'SR-002', N'اتاق سرور فرعی'),
(N'دفتر IT - طبقه 2', N'A', 2, N'IT-201', N'دفتر واحد IT'),
(N'دفتر مدیریت - طبقه 3', N'A', 3, N'MNG-301', N'دفتر مدیریت'),
(N'دفتر فروش - طبقه 1', N'B', 1, N'SAL-101', N'دفتر فروش');

-- کاربران نمونه
INSERT INTO users (username, email, full_name, department_id, is_admin, ad_user_id) VALUES
(N'admin', N'admin@company.com', N'مدیر سیستم', 1, 1, N'admin@company.com'),
(N'it_manager', N'it. manager@company.com', N'مدیر IT', 1, 1, N'it. manager@company.com'),
(N'hr_manager', N'hr.manager@company.com', N'مدیر منابع انسانی', 2, 0, N'hr.manager@company.com'),
(N'finance_manager', N'finance@company.com', N'مدیر مالی', 3, 0, N'finance@company.com');

-- دارایی‌های نمونه
INSERT INTO assets (asset_number, name, description, category_id, asset_type, status, purchase_date, purchase_price, owner_id, department_id, location_id, serial_number, model, manufacturer) VALUES
(N'ASSET-001', N'سرور اصلی', N'سرور اصلی شرکت', 1, N'Physical Server', N'فعال', '2022-01-15', 50000, 2, 1, 1, N'SN123456', N'PowerEdge R750', N'Dell'),
(N'ASSET-002', N'فایروال Palo Alto', N'فایروال اصلی', 3, N'Firewall', N'فعال', '2022-06-20', 30000, 2, 1, 1, N'PA-SN789012', N'PA-5220', N'Palo Alto'),
(N'ASSET-003', N'لپ‌تاپ مدیر IT', N'لپ‌تاپ مدیر IT', 6, N'Laptop', N'فعال', '2023-03-10', 15000, 2, 1, 3, N'LP-SN345678', N'ThinkPad X1', N'Lenovo'),
(N'ASSET-004', N'تلفن IP - دفتر 1', N'تلفن IP', 5, N'Phone', N'فعال', '2021-09-05', 2000, 3, 2, 4, N'PH-SN901234', N'CP-7941G', N'Cisco');

-- تاریخچه نمونه
INSERT INTO asset_histories (asset_id, user_id, change_type, old_value, new_value, description) VALUES
(1, 2, N'ایجاد دارایی', N'', N'سرور اصلی', N'دارایی جدید ایجاد شد'),
(3, 2, N'نقل مکان', N'دفتر IT - طبقه 2', N'دفتر مدیریت - طبقه 3', N'نقل مکان انجام شد'),
(4, 3, N'تغییر وضعیت', N'فعال', N'غیرفعال', N'دستگاه خراب شد');

-- ایجاد یک View برای آمار کلی
CREATE VIEW vw_asset_statistics AS
SELECT
    COUNT(*) as total_assets,
    SUM(CASE WHEN status = N'فعال' THEN 1 ELSE 0 END) as active_assets,
    SUM(CASE WHEN status = N'غیرفعال' THEN 1 ELSE 0 END) as inactive_assets,
    SUM(CASE WHEN status = N'تعمیر و نگهداری' THEN 1 ELSE 0 END) as maintenance_assets,
    SUM(purchase_price) as total_value,
    COUNT(DISTINCT department_id) as total_departments
FROM assets;

GO

-- ایجاد یک View برای دارایی‌های هر واحد
CREATE VIEW vw_department_assets AS
SELECT
    d.id,
    d.name as department_name,
    COUNT(a.id) as asset_count,
    SUM(a.purchase_price) as department_total_value,
    SUM(CASE WHEN a. status = N'فعال' THEN 1 ELSE 0 END) as active_count
FROM departments d
LEFT JOIN assets a ON d.id = a.department_id
GROUP BY d.id, d.name;

GO

PRINT N'پایگاه‌داده ایجاد شد! ';
