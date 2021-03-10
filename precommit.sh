#!/bin/bash

# ------ Variables

CLR_RED=[31m
CLR_GRN=[32m
CLR_CYN=[36m
CLR_NC=[0m

# ------ Functions

run_cmd_exit_on_err() {
  if ! $1; then
    echo "${CLR_RED}Error @ $2${CLR_NC}"
    read -p "Press enter to continue." -r
    exit 1
  fi
}

# ------ Code linting

echo "${CLR_CYN}Checking with pydocstyle (app)...${CLR_NC}"
run_cmd_exit_on_err "pydocstyle app --count" "pydocstyle check (app)"

echo "${CLR_CYN}Checking with flake8 (app)...${CLR_NC}"
run_cmd_exit_on_err "flake8 app --count" "flake8 check (app)"

echo "${CLR_CYN}Checking with bandit (app)...${CLR_NC}"
run_cmd_exit_on_err "bandit -r app" "bandit check (app)"

echo "${CLR_CYN}Checking with pylint (app)...${CLR_NC}"
run_cmd_exit_on_err "pylint app" "pylint check (app)"

echo "${CLR_CYN}Running code tests...${CLR_NC}"
run_cmd_exit_on_err "pytest --all" "code test"

echo "--- ${CLR_GRN}All checks passed.${CLR_NC} ---"
read -p "Press enter to continue." -r
