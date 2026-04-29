
DROP VIEW IF EXISTS vw_operational_metrics_daily CASCADE;
DROP VIEW IF EXISTS vw_operational_metrics CASCADE;
DROP TABLE IF EXISTS incidents CASCADE;


CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    incident_date DATE NOT NULL,
    severity INTEGER CHECK (severity BETWEEN 1 AND 3),
    resolution_time_minutes INTEGER  NOT NULL,
    sla_target_minutes INTEGER  NOT NULL
);

CREATE VIEW vw_operational_metrics AS
SELECT
severity,
COUNT(*) AS total_incidents,
AVG(resolution_time_minutes)::numeric(10,2) AS avg_resolution,
AVG(sla_target_minutes)::numeric(10,2) AS avg_sla_target,

AVG(
CASE
WHEN resolution_time_minutes <= sla_target_minutes
THEN 100
ELSE 0
END
)::numeric(10,2) AS sla_compliance,

PERCENTILE_CONT(0.95)
WITHIN GROUP (ORDER BY resolution_time_minutes)
::numeric(10,2) AS p95_resolution

FROM incidents
GROUP BY severity;


CREATE VIEW vw_operational_metrics_daily AS
SELECT
incident_date AS day,
severity,
COUNT(*) AS total_incidents,

AVG(resolution_time_minutes)::numeric(10,2)
AS avg_resolution,

AVG(sla_target_minutes)::numeric(10,2)
AS avg_sla_target,

AVG(
CASE
WHEN resolution_time_minutes <= sla_target_minutes
THEN 100
ELSE 0
END
)::numeric(10,2)
AS sla_compliance

FROM incidents
GROUP BY incident_date, severity
ORDER BY incident_date, severity;
