CREATE TABLE tbl_invoices (
    id INT IDENTITY(1,1) PRIMARY KEY,
    attachment_id INT,
    email_id INT NOT NULL,
    invoice_number NVARCHAR(100),
    invoice_date DATE,
    vendor_name NVARCHAR(255),
    total_amount DECIMAL(18,2),
    currency NVARCHAR(10) DEFAULT 'USD',
    line_items NVARCHAR(MAX),  -- JSON array
    extracted_data NVARCHAR(MAX),  -- JSON object
    confidence_score DECIMAL(5,4),
    verification_status NVARCHAR(50),
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (attachment_id) REFERENCES tbl_attachments(id),
    FOREIGN KEY (email_id) REFERENCES tbl_claims_emails(id),
    INDEX idx_invoice_number (invoice_number),
    INDEX idx_invoice_date (invoice_date)
);
