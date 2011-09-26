#
# Regular cron jobs for the elb-tool package
#
0 4	* * *	root	[ -x /usr/bin/elb-tool_maintenance ] && /usr/bin/elb-tool_maintenance
