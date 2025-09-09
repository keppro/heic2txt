#!/usr/bin/env python3
"""
Domain-specific custom words for Terraform, Ansible, AWS, PostgreSQL, and MySQL.

This script provides comprehensive custom word lists for different domains
to improve Apple Vision OCR recognition accuracy.
"""

from typing import List, Dict

def get_terraform_custom_words() -> List[str]:
    """Get custom words for Terraform infrastructure content."""
    return [
        # Terraform core
        "terraform", "provider", "resource", "variable", "output", "module",
        "data", "locals", "for_each", "count", "depends_on", "lifecycle",
        "backend", "state", "workspace", "environment", "configuration",
        "version", "required_version", "required_providers", "source",
        "terraform_required_version", "terraform_version", "lock",
        
        # Terraform functions
        "lookup", "merge", "keys", "values", "length", "split", "join",
        "replace", "substr", "upper", "lower", "title", "format", "formatlist",
        "file", "templatefile", "jsonencode", "yamlencode", "base64encode",
        "base64decode", "urlencode", "urldecode", "md5", "sha1", "sha256",
        "sha512", "bcrypt", "timestamp", "timeadd", "timecmp", "timeadd",
        "timecmp", "timeadd", "timecmp", "timeadd", "timecmp",
        
        # Terraform data sources
        "data_source", "aws_ami", "aws_availability_zones", "aws_caller_identity",
        "aws_region", "aws_vpc", "aws_subnet", "aws_security_group",
        "aws_instance", "aws_ebs_volume", "aws_ebs_snapshot", "aws_key_pair",
        
        # File extensions and formats
        "tf", "tfvars", "tfstate", "hcl", "json", "yaml", "yml", "toml",
        "tfplan", "tfstate.backup", "tfstate.lock.info"
    ]

def get_ansible_custom_words() -> List[str]:
    """Get custom words for Ansible automation content."""
    return [
        # Ansible core
        "ansible", "playbook", "inventory", "hosts", "vars", "tasks", "handlers",
        "roles", "templates", "files", "handlers", "meta", "defaults",
        "ansible_playbook", "ansible_play", "ansible_task", "ansible_handler",
        
        # Ansible modules
        "apt", "yum", "dnf", "package", "service", "systemd", "systemctl",
        "user", "group", "file", "copy", "template", "lineinfile", "replace",
        "command", "shell", "script", "raw", "fetch", "get_url", "unarchive",
        "archive", "cron", "at", "mount", "filesystem", "lvg", "lvol",
        "mysql_user", "mysql_db", "mysql_variables", "mysql_replication",
        "postgresql_user", "postgresql_db", "postgresql_query",
        "docker_container", "docker_image", "docker_network", "docker_volume",
        "kubernetes", "k8s", "kubectl", "helm", "istio",
        
        # Ansible collections
        "community", "ansible", "kubernetes", "docker", "mysql", "postgresql",
        "aws", "azure", "gcp", "vmware", "cisco", "juniper", "f5",
        
        # Ansible variables and facts
        "ansible_hostname", "ansible_fqdn", "ansible_architecture", "ansible_os_family",
        "ansible_distribution", "ansible_distribution_version", "ansible_memtotal_mb",
        "ansible_processor_cores", "ansible_processor_vcpus", "ansible_default_ipv4",
        "ansible_all_ipv4_addresses", "ansible_all_ipv6_addresses",
        
        # Ansible configuration
        "ansible_cfg", "ansible_config", "host_key_checking", "retry_files_enabled",
        "gathering", "fact_caching", "fact_caching_connection", "fact_caching_timeout",
        "stdout_callback", "stderr_callback", "callback_whitelist", "callback_plugins",
        
        # File extensions
        "yml", "yaml", "json", "ini", "cfg", "conf", "j2", "jinja2"
    ]

def get_aws_custom_words() -> List[str]:
    """Get custom words for AWS cloud content."""
    return [
        # AWS core services
        "aws", "amazon", "cloud", "cloudformation", "cloudwatch", "cloudtrail",
        "cloudfront", "cloudsearch", "cloudhsm", "clouddirectory",
        
        # Compute services
        "ec2", "elastic", "compute", "cloud", "instance", "ami", "ebs", "snapshot",
        "launch_template", "launch_configuration", "autoscaling", "asg",
        "lambda", "serverless", "function", "runtime", "layer", "event",
        "eventbridge", "stepfunctions", "states", "fargate", "ecs", "eks",
        "container", "docker", "image", "registry", "ecr", "repository",
        
        # Storage services
        "s3", "bucket", "object", "key", "prefix", "versioning", "lifecycle",
        "glacier", "deep_archive", "intelligent_tiering", "transfer_acceleration",
        "cloudfront", "distribution", "origin", "cache", "invalidation",
        "efs", "elastic", "file", "system", "nfs", "throughput", "mode",
        "fsx", "lustre", "windows", "file", "server", "ontap", "openzfs",
        
        # Database services
        "rds", "aurora", "mysql", "postgresql", "oracle", "sql", "server",
        "mariadb", "engine", "version", "instance", "class", "storage",
        "backup", "retention", "snapshot", "restore", "point", "time",
        "recovery", "multi_az", "read", "replica", "cluster", "endpoint",
        "dynamodb", "table", "item", "attribute", "key", "sort", "partition",
        "gsi", "lsi", "index", "query", "scan", "filter", "expression",
        "elasticache", "redis", "memcached", "cluster", "node", "group",
        "redshift", "warehouse", "cluster", "node", "type", "dc1", "dc2",
        "ra3", "serverless", "workgroup", "namespace", "database", "schema",
        
        # Networking services
        "vpc", "virtual", "private", "cloud", "subnet", "public", "private",
        "route_table", "route", "gateway", "internet", "nat", "vpn", "directconnect",
        "transit", "peering", "endpoint", "interface", "gateway", "load",
        "balancer", "application", "network", "classic", "target", "group",
        "listener", "rule", "condition", "action", "forward", "redirect",
        "fixed_response", "authenticate", "cognito", "oidc", "saml",
        
        # Security services
        "iam", "identity", "access", "management", "user", "group", "role",
        "policy", "document", "statement", "effect", "action", "resource",
        "condition", "principal", "assume", "role", "policy", "document",
        "kms", "key", "management", "service", "encryption", "decryption",
        "symmetric", "asymmetric", "customer", "managed", "aws", "managed",
        "secrets", "manager", "secret", "rotation", "lambda", "function",
        "ssm", "systems", "manager", "parameter", "store", "patch", "manager",
        "session", "manager", "run", "command", "send", "command", "start",
        "session", "document", "automation", "state", "manager",
        
        # Monitoring and logging
        "cloudwatch", "logs", "log", "group", "stream", "event", "rule",
        "schedule", "expression", "cron", "rate", "metric", "alarm", "threshold",
        "statistic", "period", "evaluation", "periods", "datapoints", "to",
        "alarm", "insights", "query", "dashboard", "widget", "graph", "number",
        "text", "log", "table", "pie", "chart", "bar", "line", "area",
        "xray", "tracing", "trace", "segment", "subsegment", "annotation",
        "metadata", "sampling", "rule", "throttle", "reservoir", "quota",
        
        # Management and governance
        "organizations", "account", "ou", "organizational", "unit", "root",
        "policy", "type", "service", "control", "scp", "tag", "policy",
        "cost", "explorer", "budgets", "budget", "alert", "threshold",
        "forecast", "anomaly", "detection", "recommendations", "trusted",
        "advisor", "support", "case", "severity", "urgent", "high", "normal",
        "low", "technical", "account", "manager", "tam", "enterprise",
        "support", "business", "support", "developer", "support", "basic",
        "support", "free", "tier", "limits", "quotas", "service", "limits",
        
        # File extensions and formats
        "json", "yaml", "yml", "tf", "tfvars", "tfstate", "hcl", "toml",
        "cfg", "conf", "ini", "properties", "env", "environment"
    ]

def get_postgresql_custom_words() -> List[str]:
    """Get custom words for PostgreSQL database content."""
    return [
        # PostgreSQL core
        "postgresql", "postgres", "psql", "database", "db", "sql", "query",
        "table", "column", "row", "record", "field", "value", "data",
        "type", "datatype", "integer", "int", "bigint", "smallint", "serial",
        "bigserial", "smallserial", "numeric", "decimal", "real", "double",
        "precision", "money", "character", "varying", "varchar", "char",
        "text", "bytea", "boolean", "bool", "date", "time", "timestamp",
        "timestamptz", "interval", "json", "jsonb", "xml", "uuid", "array",
        "composite", "range", "multirange", "domain", "enum", "set",
        
        # PostgreSQL data types
        "int2", "int4", "int8", "float4", "float8", "oid", "regproc",
        "regprocedure", "regoper", "regoperator", "regclass", "regtype",
        "regrole", "regnamespace", "regconfig", "regdictionary", "cidr",
        "inet", "macaddr", "macaddr8", "bit", "varbit", "tsvector",
        "tsquery", "ltree", "lquery", "ltxtquery", "path", "polygon",
        "circle", "line", "lseg", "box", "point", "pg_lsn", "txid_snapshot",
        
        # PostgreSQL functions
        "select", "insert", "update", "delete", "create", "drop", "alter",
        "grant", "revoke", "begin", "commit", "rollback", "savepoint",
        "release", "set", "show", "explain", "analyze", "vacuum", "reindex",
        "cluster", "truncate", "copy", "load", "unload", "import", "export",
        
        # PostgreSQL clauses
        "from", "where", "group", "by", "having", "order", "limit", "offset",
        "distinct", "all", "union", "intersect", "except", "with", "recursive",
        "as", "alias", "inner", "left", "right", "full", "outer", "join",
        "on", "using", "natural", "cross", "exists", "in", "not", "null",
        "is", "between", "like", "ilike", "similar", "to", "regexp", "match",
        "and", "or", "case", "when", "then", "else", "end", "if", "coalesce",
        "nullif", "greatest", "least", "cast", "convert", "extract", "date_part",
        
        # PostgreSQL operators
        "=", "!=", "<>", "<", ">", "<=", ">=", "+", "-", "*", "/", "%", "^",
        "|", "&", "#", "~", "!~", "~*", "!~*", "||", "->", "->>", "#>", "#>>",
        "@>", "<@", "?", "?&", "?|", "&&", "||", "&<", "&>", "<<", ">>", "<<=",
        ">>=", "~=", "is", "isnot", "isnull", "notnull", "true", "false",
        "unknown", "null", "unknown", "true", "false", "null",
        
        # PostgreSQL aggregates
        "count", "sum", "avg", "min", "max", "stddev", "variance", "stddev_pop",
        "variance_pop", "stddev_samp", "variance_samp", "array_agg", "string_agg",
        "json_agg", "jsonb_agg", "json_object_agg", "jsonb_object_agg",
        "xmlagg", "corr", "covar_pop", "covar_samp", "regr_avgx", "regr_avgy",
        "regr_count", "regr_intercept", "regr_r2", "regr_slope", "regr_sxx",
        "regr_sxy", "regr_syy", "bit_and", "bit_or", "bit_xor", "bool_and",
        "bool_or", "every", "mode", "percentile_cont", "percentile_disc",
        "percent_rank", "cume_dist", "dense_rank", "rank", "row_number",
        "lag", "lead", "first_value", "last_value", "nth_value", "ntile",
        
        # PostgreSQL system functions
        "current_database", "current_user", "session_user", "user", "version",
        "pg_version", "pg_database_size", "pg_relation_size", "pg_total_relation_size",
        "pg_size_pretty", "pg_stat_get_db_*", "pg_stat_get_tuples_*",
        "pg_stat_get_blocks_*", "pg_stat_get_live_tuples", "pg_stat_get_dead_tuples",
        "pg_stat_get_blocks_hit", "pg_stat_get_blocks_read", "pg_stat_get_tuples_*",
        "pg_stat_get_blocks_*", "pg_stat_get_live_tuples", "pg_stat_get_dead_tuples",
        
        # PostgreSQL configuration
        "postgresql_conf", "postgresql_auto_conf", "pg_hba_conf", "pg_ident_conf",
        "shared_preload_libraries", "max_connections", "shared_buffers",
        "effective_cache_size", "work_mem", "maintenance_work_mem", "wal_buffers",
        "checkpoint_segments", "checkpoint_completion_target", "wal_level",
        "archive_mode", "archive_command", "max_wal_senders", "hot_standby",
        "synchronous_commit", "fsync", "full_page_writes", "wal_compression",
        "wal_log_hints", "track_activities", "track_counts", "track_io_timing",
        "track_functions", "log_statement", "log_min_duration_statement",
        "log_line_prefix", "log_checkpoints", "log_connections", "log_disconnections",
        "log_lock_waits", "log_temp_files", "log_autovacuum_min_duration",
        "log_error_verbosity", "log_min_messages", "log_min_error_statement",
        "log_min_duration_statement", "log_statement_stats", "log_parser_stats",
        "log_planner_stats", "log_executor_stats", "log_statement_stats",
        
        # PostgreSQL extensions
        "extension", "create_extension", "drop_extension", "alter_extension",
        "pg_stat_statements", "pg_buffercache", "pg_freespacemap", "pg_hint_plan",
        "pg_qualstats", "pg_stat_kcache", "pg_stat_statements", "pg_wait_sampling",
        "pg_audit", "pgaudit", "pglogical", "pglogical_origin", "pglogical_replication",
        "pglogical_sync", "pglogical_ticker", "pglogical_ticker", "pglogical_ticker",
        "postgis", "postgis_topology", "postgis_sfcgal", "postgis_tiger_geocoder",
        "postgis_raster", "postgis_sfcgal", "postgis_tiger_geocoder", "postgis_raster",
        "uuid_ossp", "uuid_generate_v1", "uuid_generate_v4", "uuid_generate_v5",
        "uuid_nil", "uuid_ns_dns", "uuid_ns_url", "uuid_ns_oid", "uuid_ns_x500",
        "uuid_ns_dns", "uuid_ns_url", "uuid_ns_oid", "uuid_ns_x500", "uuid_ns_dns",
        
        # File extensions
        "sql", "dump", "backup", "restore", "pg_dump", "pg_restore", "psql",
        "conf", "log", "pid", "lock", "tmp", "temp", "wal", "archive"
    ]

def get_mysql_custom_words() -> List[str]:
    """Get custom words for MySQL database content."""
    return [
        # MySQL core
        "mysql", "mariadb", "database", "db", "sql", "query", "table",
        "column", "row", "record", "field", "value", "data", "type",
        "datatype", "integer", "int", "bigint", "smallint", "tinyint",
        "mediumint", "serial", "bigserial", "smallserial", "decimal",
        "numeric", "float", "double", "real", "precision", "scale",
        "bit", "boolean", "bool", "char", "varchar", "binary", "varbinary",
        "tinyblob", "blob", "mediumblob", "longblob", "tinytext", "text",
        "mediumtext", "longtext", "enum", "set", "date", "time", "datetime",
        "timestamp", "year", "json", "geometry", "point", "linestring",
        "polygon", "multipoint", "multilinestring", "multipolygon",
        "geometrycollection", "spatial", "index", "rtree", "btree", "hash",
        
        # MySQL data types
        "int1", "int2", "int3", "int4", "int8", "int11", "int21", "int24",
        "int32", "int64", "float4", "float8", "double_precision", "real",
        "dec", "fixed", "numeric", "decimal", "bit", "bool", "boolean",
        "char", "varchar", "binary", "varbinary", "tinyblob", "blob",
        "mediumblob", "longblob", "tinytext", "text", "mediumtext",
        "longtext", "enum", "set", "date", "time", "datetime", "timestamp",
        "year", "json", "geometry", "point", "linestring", "polygon",
        "multipoint", "multilinestring", "multipolygon", "geometrycollection",
        
        # MySQL functions
        "select", "insert", "update", "delete", "create", "drop", "alter",
        "grant", "revoke", "begin", "commit", "rollback", "savepoint",
        "release", "set", "show", "explain", "describe", "desc", "analyze",
        "optimize", "repair", "check", "checksum", "truncate", "load",
        "unload", "import", "export", "backup", "restore", "dump", "load",
        
        # MySQL clauses
        "from", "where", "group", "by", "having", "order", "limit", "offset",
        "distinct", "all", "union", "intersect", "except", "with", "recursive",
        "as", "alias", "inner", "left", "right", "full", "outer", "join",
        "on", "using", "natural", "cross", "exists", "in", "not", "null",
        "is", "between", "like", "regexp", "rlike", "match", "against",
        "and", "or", "case", "when", "then", "else", "end", "if", "ifnull",
        "coalesce", "nullif", "greatest", "least", "cast", "convert",
        "extract", "date_format", "time_format", "str_to_date", "date_add",
        "date_sub", "adddate", "subdate", "addtime", "subtime", "datediff",
        "timediff", "timestampdiff", "timestampadd", "from_unixtime",
        "unix_timestamp", "now", "curdate", "curtime", "sysdate", "utc_date",
        "utc_time", "utc_timestamp", "year", "month", "day", "hour", "minute",
        "second", "microsecond", "week", "weekday", "weekofyear", "dayofyear",
        "dayofweek", "dayofmonth", "monthname", "dayname", "quarter",
        
        # MySQL operators
        "=", "!=", "<>", "<", ">", "<=", ">=", "<=>", "+", "-", "*", "/", "%",
        "div", "mod", "&", "|", "^", "~", "<<" ">>", "&&", "||", "xor",
        "not", "and", "or", "is", "isnot", "isnull", "notnull", "true",
        "false", "unknown", "null", "unknown", "true", "false", "null",
        
        # MySQL aggregates
        "count", "sum", "avg", "min", "max", "std", "stddev", "variance",
        "stddev_pop", "variance_pop", "stddev_samp", "variance_samp",
        "group_concat", "bit_and", "bit_or", "bit_xor", "json_arrayagg",
        "json_objectagg", "json_array", "json_object", "json_quote",
        "json_unquote", "json_extract", "json_keys", "json_length",
        "json_contains", "json_contains_path", "json_overlaps", "json_search",
        "json_value", "json_table", "json_merge_patch", "json_merge_preserve",
        "json_remove", "json_replace", "json_set", "json_insert", "json_append",
        "json_merge", "json_merge_preserve", "json_merge_patch", "json_remove",
        "json_replace", "json_set", "json_insert", "json_append", "json_merge",
        
        # MySQL system functions
        "database", "schema", "user", "current_user", "session_user",
        "system_user", "version", "connection_id", "last_insert_id",
        "row_count", "found_rows", "affected_rows", "insert_id", "charset",
        "collation", "collation_connection", "collation_database",
        "collation_server", "default_character_set_name", "default_collation_name",
        "character_set_client", "character_set_connection", "character_set_database",
        "character_set_filesystem", "character_set_results", "character_set_server",
        "character_set_system", "character_sets_dir", "collation_connection",
        "collation_database", "collation_server", "init_connect", "init_file",
        "init_slave", "interactive_timeout", "join_buffer_size", "key_buffer_size",
        "key_cache_age_threshold", "key_cache_block_size", "key_cache_division_limit",
        "key_cache_file_hash_table_size", "key_cache_segments", "key_read_requests",
        "key_reads", "key_write_requests", "key_writes", "language", "large_files_support",
        "large_page_size", "large_pages", "last_insert_id", "lc_messages",
        "lc_messages_dir", "lc_time_names", "license", "local_infile", "locked_in_memory",
        "log", "log_bin", "log_bin_basename", "log_bin_index", "log_bin_trust_function_creators",
        "log_bin_use_v1_row_events", "log_error", "log_error_services", "log_error_suppression_list",
        "log_error_verbosity", "log_output", "log_queries_not_using_indexes",
        "log_slave_updates", "log_slow_admin_statements", "log_slow_extra",
        "log_slow_slave_statements", "log_statements", "log_syslog", "log_syslog_facility",
        "log_syslog_include_pid", "log_syslog_tag", "log_throttle_queries_not_using_indexes",
        "log_timestamps", "log_warnings", "long_query_time", "low_priority_updates",
        "lower_case_file_system", "lower_case_table_names", "maintainer_mode",
        "master_info_repository", "master_verify_checksum", "max_allowed_packet",
        "max_binlog_cache_size", "max_binlog_size", "max_binlog_stmt_cache_size",
        "max_connect_errors", "max_connections", "max_delayed_threads", "max_error_count",
        "max_execution_time", "max_heap_table_size", "max_insert_delayed_threads",
        "max_join_size", "max_length_for_sort_data", "max_points_in_geometry",
        "max_prepared_stmt_count", "max_relay_log_size", "max_seeks_for_key",
        "max_sort_length", "max_sp_recursion_depth", "max_tmp_tables", "max_user_connections",
        "max_write_lock_count", "metadata_locks_cache_size", "metadata_locks_hash_instances",
        "min_examined_row_limit", "myisam_data_pointer_size", "myisam_max_sort_file_size",
        "myisam_mmap_size", "myisam_recover_options", "myisam_repair_threads",
        "myisam_sort_buffer_size", "myisam_stats_method", "myisam_use_mmap",
        "mysql_native_password", "named_pipe", "net_buffer_length", "net_read_timeout",
        "net_retry_count", "net_write_timeout", "new", "ngram_token_size",
        "offline_mode", "old", "old_alter_table", "old_passwords", "open_files_limit",
        "optimizer_prune_level", "optimizer_search_depth", "optimizer_switch",
        "optimizer_trace", "optimizer_trace_features", "optimizer_trace_limit",
        "optimizer_trace_max_mem_size", "optimizer_trace_offset", "parser_max_mem_size",
        "performance_schema", "performance_schema_accounts_size", "performance_schema_digests_size",
        "performance_schema_events_stages_history_long_size", "performance_schema_events_stages_history_size",
        "performance_schema_events_statements_history_long_size", "performance_schema_events_statements_history_size",
        "performance_schema_events_transactions_history_long_size", "performance_schema_events_transactions_history_size",
        "performance_schema_events_waits_history_long_size", "performance_schema_events_waits_history_size",
        "performance_schema_hosts_size", "performance_schema_max_cond_instances",
        "performance_schema_max_cond_instances", "performance_schema_max_file_instances",
        "performance_schema_max_file_instances", "performance_schema_max_mutex_instances",
        "performance_schema_max_mutex_instances", "performance_schema_max_rwlock_instances",
        "performance_schema_max_rwlock_instances", "performance_schema_max_socket_instances",
        "performance_schema_max_socket_instances", "performance_schema_max_table_instances",
        "performance_schema_max_table_instances", "performance_schema_max_table_handles",
        "performance_schema_max_table_handles", "performance_schema_max_thread_instances",
        "performance_schema_max_thread_instances", "performance_schema_session_connect_attrs_size",
        "performance_schema_users_size", "pid_file", "plugin_dir", "port", "preload_buffer_size",
        "profiling", "profiling_history_size", "protocol_version", "proxy_user", "pseudo_slave_mode",
        "pseudo_thread_id", "query_alloc_block_size", "query_cache_limit", "query_cache_min_res_unit",
        "query_cache_size", "query_cache_type", "query_prealloc_size", "rand_seed1", "rand_seed2",
        "range_alloc_block_size", "rbr_exec_mode", "read_buffer_size", "read_only", "read_rnd_buffer_size",
        "relay_log", "relay_log_basename", "relay_log_index", "relay_log_info_file", "relay_log_info_repository",
        "relay_log_purge", "relay_log_recovery", "relay_log_space_limit", "replicate_annotate_row_events",
        "replicate_do_db", "replicate_do_table", "replicate_ignore_db", "replicate_ignore_table",
        "replicate_rewrite_db", "replicate_wild_do_table", "replicate_wild_ignore_table",
        "replication_optimize_for_static_plugin_config", "replication_sender_observe_commit_only",
        "report_host", "report_password", "report_port", "report_user", "require_secure_transport",
        "rpl_semi_sync_master_enabled", "rpl_semi_sync_master_timeout", "rpl_semi_sync_master_trace_level",
        "rpl_semi_sync_master_wait_for_slave_count", "rpl_semi_sync_master_wait_no_slave",
        "rpl_semi_sync_slave_enabled", "rpl_semi_sync_slave_trace_level", "rpl_stop_slave_timeout",
        "safe_user_create", "secure_auth", "secure_file_priv", "server_id", "server_id_bits",
        "session_track_gtids", "session_track_schema", "session_track_state_change",
        "session_track_system_variables", "session_track_transaction_info", "sha256_password_auto_generate_rsa_keys",
        "sha256_password_private_key_path", "sha256_password_public_key_path", "show_compatibility_56",
        "show_old_temporals", "skip_external_locking", "skip_name_resolve", "skip_networking",
        "skip_show_database", "slave_allow_batching", "slave_checkpoint_group", "slave_checkpoint_period",
        "slave_compressed_protocol", "slave_exec_mode", "slave_load_tmpdir", "slave_max_allowed_packet",
        "slave_net_timeout", "slave_parallel_workers", "slave_pending_jobs_size_max",
        "slave_preserve_commit_order", "slave_rows_search_algorithms", "slave_skip_errors",
        "slave_sql_verify_checksum", "slave_transaction_retries", "slave_type_conversions",
        "slow_launch_time", "slow_query_log", "slow_query_log_file", "socket", "sort_buffer_size",
        "sql_auto_is_null", "sql_big_selects", "sql_big_tables", "sql_buffer_result",
        "sql_log_bin", "sql_log_off", "sql_log_update", "sql_low_priority_updates",
        "sql_mode", "sql_notes", "sql_quote_show_create", "sql_safe_updates", "sql_select_limit",
        "sql_slave_skip_counter", "sql_warnings", "ssl_ca", "ssl_capath", "ssl_cert", "ssl_cipher",
        "ssl_crl", "ssl_crlpath", "ssl_key", "ssl_verify_server_cert", "stored_program_cache",
        "stored_program_definition_cache", "super_read_only", "sync_binlog", "sync_frm",
        "sync_master_info", "sync_relay_log", "sync_relay_log_info", "system_time_zone",
        "table_definition_cache", "table_open_cache", "table_open_cache_instances",
        "thread_cache_size", "thread_handling", "thread_stack", "time_zone", "timestamp",
        "tls_version", "tmp_table_size", "tmpdir", "transaction_alloc_block_size",
        "transaction_prealloc_size", "transaction_read_only", "transaction_write_set_extraction",
        "tx_isolation", "tx_read_only", "unique_checks", "updatable_views_with_limit",
        "upgrade", "use_old_alter_table", "user", "version", "version_comment",
        "version_compile_machine", "version_compile_os", "version_malloc_library",
        "version_ssl_library", "wait_timeout", "warning_count", "windowing_use_high_precision",
        "wsrep_auto_increment_control", "wsrep_causal_reads", "wsrep_certify_nonpk",
        "wsrep_cluster_address", "wsrep_cluster_name", "wsrep_convert_lock_to_trx",
        "wsrep_data_home_dir", "wsrep_debug", "wsrep_desync", "wsrep_dirty_reads",
        "wsrep_drupal_282555_workaround", "wsrep_forced_binlog_format", "wsrep_gtid_domain_id",
        "wsrep_gtid_mode", "wsrep_load_data_splitting", "wsrep_log_conflicts",
        "wsrep_max_ws_rows", "wsrep_max_ws_size", "wsrep_mysql_replication_bundle",
        "wsrep_node_address", "wsrep_node_incoming_address", "wsrep_node_name",
        "wsrep_notify_cmd", "wsrep_on", "wsrep_osu_method", "wsrep_patch_version",
        "wsrep_provider", "wsrep_provider_options", "wsrep_recover", "wsrep_replicate_myisam",
        "wsrep_retry_autocommit", "wsrep_slave_fk_checks", "wsrep_slave_uk_checks",
        "wsrep_slave_threads", "wsrep_sst_auth", "wsrep_sst_donor", "wsrep_sst_donor_rejects_queries",
        "wsrep_sst_method", "wsrep_sst_receive_address", "wsrep_start_position",
        "wsrep_sync_wait", "wsrep_trx_fragment_size", "wsrep_trx_fragment_unit",
        "wsrep_wsrep_ready", "wsrep_wsrep_wsrep_ready", "wsrep_wsrep_wsrep_wsrep_ready",
        
        # File extensions
        "sql", "dump", "backup", "restore", "mysqldump", "mysql", "mysqladmin",
        "mysqlcheck", "mysqlimport", "mysqlshow", "mysqlslap", "mysql_upgrade",
        "conf", "ini", "cnf", "log", "pid", "lock", "tmp", "temp", "sock"
    ]

def get_combined_custom_words() -> List[str]:
    """Get combined custom words from all domains."""
    all_words = []
    all_words.extend(get_terraform_custom_words())
    all_words.extend(get_ansible_custom_words())
    all_words.extend(get_aws_custom_words())
    all_words.extend(get_postgresql_custom_words())
    all_words.extend(get_mysql_custom_words())
    
    # Remove duplicates while preserving order
    seen = set()
    unique_words = []
    for word in all_words:
        if word not in seen:
            seen.add(word)
            unique_words.append(word)
    
    return unique_words

def get_domain_specific_words(domains: List[str]) -> List[str]:
    """Get custom words for specific domains."""
    domain_functions = {
        'terraform': get_terraform_custom_words,
        'ansible': get_ansible_custom_words,
        'aws': get_aws_custom_words,
        'postgresql': get_postgresql_custom_words,
        'mysql': get_mysql_custom_words
    }
    
    all_words = []
    for domain in domains:
        if domain.lower() in domain_functions:
            all_words.extend(domain_functions[domain.lower()]())
    
    # Remove duplicates while preserving order
    seen = set()
    unique_words = []
    for word in all_words:
        if word not in seen:
            seen.add(word)
            unique_words.append(word)
    
    return unique_words

def print_domain_stats():
    """Print statistics for each domain's custom words."""
    domains = {
        'Terraform': get_terraform_custom_words(),
        'Ansible': get_ansible_custom_words(),
        'AWS': get_aws_custom_words(),
        'PostgreSQL': get_postgresql_custom_words(),
        'MySQL': get_mysql_custom_words()
    }
    
    print("📊 Domain-Specific Custom Words Statistics")
    print("=" * 50)
    
    total_words = 0
    for domain, words in domains.items():
        print(f"{domain:12}: {len(words):4} words")
        total_words += len(words)
    
    print("-" * 50)
    print(f"{'Total':12}: {total_words:4} words")
    print()
    
    # Show sample words from each domain
    for domain, words in domains.items():
        print(f"{domain} sample words:")
        sample_words = words[:10] if len(words) >= 10 else words
        print(f"  {', '.join(sample_words)}")
        if len(words) > 10:
            print(f"  ... and {len(words) - 10} more")
        print()

if __name__ == "__main__":
    print_domain_stats()
    
    # Example usage
    print("🎯 Example Usage:")
    print("-" * 30)
    
    # Get words for specific domains
    terraform_ansible_words = get_domain_specific_words(['terraform', 'ansible'])
    print(f"Terraform + Ansible: {len(terraform_ansible_words)} words")
    
    # Get all words
    all_words = get_combined_custom_words()
    print(f"All domains combined: {len(all_words)} words")
    
    print("\n💡 Usage in code:")
    print("```python")
    print("from domain_specific_custom_words import get_domain_specific_words")
    print("")
    print("# Get words for specific domains")
    print("custom_words = get_domain_specific_words(['terraform', 'aws', 'postgresql'])")
    print("ocr = AppleVisionOCREngine(language='en', custom_words=custom_words)")
    print("```")
