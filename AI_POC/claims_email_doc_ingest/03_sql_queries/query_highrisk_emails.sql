SELECT 
    e.id,
    e.message_id,
    e.subject,
    e.sender,
    e.email_date,
    ent.claim_number,
    ent.policy_number,
    ent.insured_name,
    ent.claim_amount,
    t.priority_level,
    t.claim_type,
    t.risk_level,
    t.triage_notes,
    t.assigned_to
FROM tbl_claims_emails e
INNER JOIN tbl_extracted_entities ent ON e.id = ent.email_id
INNER JOIN tbl_triage_results t ON e.id = t.email_id
WHERE t.requires_escalation = 1
    AND t.reviewed_at IS NULL
ORDER BY 
    CASE t.priority_level
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
        WHEN 'medium' THEN 3
        ELSE 4
    END,
    e.email_date DESC;
