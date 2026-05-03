#!/bin/bash

# SoundPilot - Run All Tests
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

FAILED_SERVICES=""

echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}  SoundPilot Test Suite${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo ""

# 1. Storage Tests
echo -e "${BLUE}[1/3] Storage Service Tests${NC}"
cd "$ROOT_DIR/backend/storage"
python3 -m pytest tests/ -v --tb=short
[ $? -ne 0 ] && FAILED_SERVICES="$FAILED_SERVICES Storage"
echo ""

# 2. Processor Tests
echo -e "${BLUE}[2/3] Processor Service Tests${NC}"
cd "$ROOT_DIR/backend/processor"
python3 -m pytest tests/ -v --tb=short
[ $? -ne 0 ] && FAILED_SERVICES="$FAILED_SERVICES Processor"
echo ""

# 3. Frontend Tests
echo -e "${BLUE}[3/3] Frontend Tests${NC}"
cd "$ROOT_DIR/frontend"
npm run test 2>&1
[ $? -ne 0 ] && FAILED_SERVICES="$FAILED_SERVICES Frontend"
echo ""

echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}  Results${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"

if [ -z "$FAILED_SERVICES" ]; then
    echo -e "  ${GREEN}✓ ALL TESTS PASSED${NC}"
else
    echo -e "  ${RED}✗ FAILED SERVICES:${NC}"
    for svc in $FAILED_SERVICES; do
        echo -e "    ${RED}• ${svc}${NC}"
    done
    echo ""
    echo -e "  ${YELLOW}Run individually for details:${NC}"
    for svc in $FAILED_SERVICES; do
        case $svc in
            Storage)   echo -e "    cd backend/storage && python3 -m pytest tests/ -v" ;;
            Processor) echo -e "    cd backend/processor && python3 -m pytest tests/ -v" ;;
            Frontend)  echo -e "    cd frontend && npm run test" ;;
        esac
    done
fi

echo -e "${BLUE}═══════════════════════════════════════${NC}"

[ -z "$FAILED_SERVICES" ] && exit 0 || exit 1
