SELECT 
    t.claim_type,
    t.risk_level,
    COUNT(*) as email_count,
    SUM(CASE WHEN t.requires_escalation = 1 THEN 1 ELSE 0 END) as escalated_count,
    AVG(CAST(ent.claim_amount AS FLOAT)) as avg_claim_amount
FROM tbl_triage_results t
INNER JOIN tbl_extracted_entities ent ON t.email_id = ent.email_id
WHERE t.created_at >= DATEADD(day, -30, GETDATE())
GROUP BY t.claim_type, t.risk_level
ORDER BY email_count DESC;
