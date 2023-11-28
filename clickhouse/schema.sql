CREATE DATABASE IF NOT EXISTS graphite;

CREATE TABLE IF NOT EXISTS graphite.graphite
(
    Path String,
    Value Float64,
    Time UInt32,
    Date Date,
    Timestamp UInt32
)
ENGINE = GraphiteMergeTree('graphite_rollup')
PARTITION BY toMonday(Date)
ORDER BY (Path, Time)
TTL Date + toIntervalMonth(25)
SETTINGS index_granularity = 8125;

-- optional table for faster metric search
CREATE TABLE IF NOT EXISTS graphite.graphite_index
(
    Date Date,
    Level UInt32,
    Path String,
    Version UInt32
)
ENGINE = ReplacingMergeTree(Version)
PARTITION BY toMonday(Date)
ORDER BY (Level, Path, Date);

-- optional table for storing Graphite tags
CREATE TABLE IF NOT EXISTS graphite.graphite_tagged
(
    Date Date,
    Tag1 String,
    Path String,
    Tags Array(String),
    Version UInt32
)
ENGINE = ReplacingMergeTree(Version)
PARTITION BY toMonday(Date)
ORDER BY (Tag1, Path, Date);
