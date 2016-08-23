#!/bin/bash

printf "[*] fixing unittests/seleniumtests with autopep8\n"
UNITTEST_PATH=./unittests
SELENIUM_PATH=./selenium
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TEXT_DIR=${DIR}/text

function usage(){
    echo "USAGE: ./testrunner.sh [selenium|unit|standalone]"
    exit 1
}

setup-failed(){
    echo "test-setup failed"
    exit 1
}

if [[ ! -x $(which autopep8) ]]; then
    echo "install autopep8!"
    setup-failed
fi

get-texts(){
    curl https://www.gutenberg.org/cache/epub/11/pg11.txt | sed -n 42,3367p > "$TEXT_DIR/base.txt"

    # empty is … well empty obviously
    touch "$TEXT_DIR/empty.txt"

    # the default is very small, only fifty lines
    head -n 50 "${TEXT_DIR}/base.txt" > "${TEXT_DIR}/deflt.txt"

    # large is five times larger than the base 
    cat "${TEXT_DIR}/base.txt" > "${TEXT_DIR}/large.txt"
    cat "${TEXT_DIR}/base.txt" >> "${TEXT_DIR}/large.txt"
    cat "${TEXT_DIR}/base.txt" >> "${TEXT_DIR}/large.txt"
    cat "${TEXT_DIR}/base.txt" >> "${TEXT_DIR}/large.txt"
    cat "${TEXT_DIR}/base.txt" >> "${TEXT_DIR}/large.txt"

    # limit.txt is huge, but below the limit
    cat "${TEXT_DIR}/base.txt" > "${TEXT_DIR}/limit.txt"
    while [[ $(ls -l "${TEXT_DIR}/limit.txt" | awk '{print $5}') -lt 3700000 ]]; do
        cat "${TEXT_DIR}/base.txt" >> "${TEXT_DIR}/limit.txt"
    done

    # crash.txt should return an error
    cat "${TEXT_DIR}/base.txt" > "${TEXT_DIR}/crash.txt"
    while [[ $(ls -l "${TEXT_DIR}/crash.txt" | awk '{print $5}') -lt 4000000 ]]; do
        cat "${TEXT_DIR}/base.txt" >> "${TEXT_DIR}/crash.txt"
    done

}

function run-standalone(){
    printf "[*] standalone checks \n"
    "${DIR}/always_return.sh"
}


function setup-selenium(){
    sample_texts="base.txt empty.txt deflt.txt large.txt limit.txt crash.txt"
    for i in $sample_texts; do
        if [[ ! -f "${TEXT_DIR}/$i" ]]; then
            echo "Testing-texts not present."
            echo "Need: ${sample_texts} in ${TEXT_DIR}"
            get-texts
        fi
    done

}

function fix-selenium(){
    setup-selenium
    if [[ ! -d "$TEXT_DIR" ]]; then
        echo "sample texts not present!"
        setup-failed
    fi
    for i in ${SELENIUM_PATH}/*.py; do
        autopep8 -i "$i"
    done
}

function run-selenium(){
    #fix-selenium
    printf "[*] running selenium tests\n"

    EXCLUDED_TESTS="CreateProject.py Tokenize.py"
    EXCLUDED_TESTS="Tokenize.py "

    for i in ${SELENIUM_PATH}/[A-Z]*.py; do 
        CONTINUE=0
        for EXCLUDE in $EXCLUDED_TESTS; do
            if [[ $i =~ $EXCLUDE ]]; then
                printf "%s is excluded!\n" "$i"
                CONTINUE=1
                break
            fi
        done
        if [[ $CONTINUE -eq 1 ]]; then
            continue
        fi
        printf "   - running test %s\n" "$i"
        $i
    done
    printf "WARNING: The following tests were excluded:\n"
    for i in $EXCLUDED_TESTS; do
        printf " - %s\n" "$i"
    done
}

function fix-unittests(){
    for i in ${UNITTEST_PATH}/*/*.py; do
        autopep8 -i "$i"
    done
}

function run-unittests(){
    #fix-unittests
    printf "[*] running unittests tests\n"

    for i in ${UNITTEST_PATH}/*/[A-Z]*.py; do 
        printf "     -  running test %s\n" "$i"
        $i
    done
}

RUN_SELENIUM=0
RUN_UNITTESTS=0

ACTION=$1
if [[ -z $ACTION ]]; then
    RUN_SELENIUM=1
    RUN_UNITTESTS=1
elif [[ $ACTION == 'unit' ]]; then
    RUN_UNITTESTS=1
elif [[ $ACTION == 'selenium' ]]; then
    RUN_SELENIUM=1
else
    usage
fi

if [[ $RUN_SELENIUM -eq 1 ]]; then
    run-selenium
fi

if [[ $RUN_UNITTESTS -eq 1  ]]; then
    run-unittests
fi

