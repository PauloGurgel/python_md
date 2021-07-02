#!/usr/bin/env bash

# -------------------------------------------------------------------
# Startup Script
# -------------------------------------------------------------------
#
# Run a list of command lines in background, monitor their execution
# and kill all the remaining processes if any of them is stopped


# Command line list
# Associative array: Friendly title => command line
# Add here each process that need to be executed

export FLASK_ENV=presentation

declare -A commands=(
    ["Flask App"]="uwsgi --ini wsgi.ini --http :5000"
)

check_interval_seconds=1

# Run each command and collect their PIDs
declare -A commands_pids
for command_title in "${!commands[@]}"; do
    echo "Starting ${command_title}"
    command_line=${commands[$command_title]}
    ($command_line) & commands_pids[$command_title]=$!
    echo -e "${command_title} PID = ${commands_pids[$command_title]}\n"
done

# Monitor execution - will stay in this loop until a process is stopped
while (( ${#commands_pids[@]} )); do
  for pid_idx in "${!commands_pids[@]}"; do
    pid=${commands_pids[$pid_idx]}
    if ! kill -0 "$pid" 2>/dev/null; then # check for process existence
      # the process has ended
      echo -e "$pid_idx (PID ${pid}) died\n"
      unset "commands_pids[$pid_idx]"
      break 2
    fi
  done
  sleep $check_interval_seconds
done

# Stop all remaining processes and terminate
echo "Stopping the remaining processes:"
for pid_idx in "${!commands_pids[@]}"; do
    pid=${commands_pids[$pid_idx]}
    echo -n "${pid_idx} (${pid})... "
    kill $pid
    echo "ok"
done
