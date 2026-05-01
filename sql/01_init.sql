-- 01_init.sql  – runs automatically on first postgres start

CREATE TABLE IF NOT EXISTS products (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(200)   NOT NULL,
    description TEXT           NOT NULL,
    price       NUMERIC(10,2)  NOT NULL,
    category    VARCHAR(100)   NOT NULL,
    stock       INTEGER        DEFAULT 0
);

-- Seed data: 20 electronics products
INSERT INTO products (name, description, price, category, stock) VALUES
('Wireless Noise-Cancelling Headphones', 'Over-ear headphones with active noise cancellation, 30h battery, Bluetooth 5.0', 149.99, 'Electronics', 45),
('Mechanical Gaming Keyboard', 'TKL layout, Cherry MX Red switches, RGB backlight, USB-C detachable cable', 89.99, 'Gaming', 120),
('4K Ultra HD Monitor 27"', 'IPS panel, 144Hz refresh rate, HDR400, USB-C and HDMI ports', 399.99, 'Monitors', 30),
('Ergonomic Wireless Mouse', 'Vertical design, 6 programmable buttons, 90-day battery life, USB dongle', 59.99, 'Peripherals', 200),
('USB-C Docking Station', '12-in-1 hub: 4K HDMI, 100W PD, 4x USB-A, SD card reader, Ethernet', 79.99, 'Accessories', 85),
('Portable Bluetooth Speaker', 'IPX7 waterproof, 360° sound, 20h playtime, built-in microphone', 49.99, 'Audio', 150),
('Webcam 1080p Full HD', 'Auto-focus, built-in stereo mic, USB plug-and-play, privacy shutter', 69.99, 'Cameras', 95),
('Laptop Stand Adjustable', 'Aluminum, 6 height levels, foldable, compatible with 10–17 inch laptops', 34.99, 'Accessories', 300),
('SSD External 1TB', 'USB 3.2 Gen2, 1050 MB/s read, shock-resistant, pocket-sized', 89.99, 'Storage', 60),
('Wireless Charging Pad 15W', 'Qi-certified, fast charge for iPhone & Android, LED indicator, slim design', 24.99, 'Charging', 400),
('Smart LED Desk Lamp', 'Touch control, 5 color temperatures, USB charging port, memory function', 39.99, 'Lighting', 110),
('Gaming Headset 7.1 Surround', 'Virtual 7.1 surround sound, retractable mic, memory foam earcups, USB', 59.99, 'Gaming', 75),
('Portable Power Bank 20000mAh', '65W USB-C PD, charges laptop and phone simultaneously, LED display', 49.99, 'Charging', 180),
('Bluetooth Trackpad', 'Multi-touch gestures, rechargeable, Windows & macOS compatible', 44.99, 'Peripherals', 90),
('Mechanical Numpad', 'Standalone number pad, hot-swap switches, RGB, USB passthrough', 29.99, 'Gaming', 140),
('Noise-Cancelling Earbuds', 'True wireless, ANC, 8h battery + 32h case, IPX4, USB-C charging', 99.99, 'Audio', 220),
('USB Microphone Cardioid', 'Studio-quality recording, plug-and-play, mute button, headphone jack', 79.99, 'Audio', 55),
('4-Port USB Hub 3.0', 'Individual power switches, LED indicators, compatible with all OS', 19.99, 'Accessories', 500),
('Smart Plug WiFi', 'Voice control via Alexa & Google, energy monitoring, schedule timer', 14.99, 'Smart Home', 350),
('Cable Management Box', 'Hides power strips and cables, bamboo lid, 3 size openings', 22.99, 'Accessories', 270);
