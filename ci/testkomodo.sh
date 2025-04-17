check_queue () {
    # Keeping this the same as
    # https://github.com/equinor/komodo-releases/blob/main/.github/workflows/run_reek_hm.yml
    set +e
    hostname
    export PATH=$PATH:/global/bin
    # /global/bin/bjobs gives an error message when run on non-shared disks.
    # Filter it away, but keep stderr as is, and error hard if bjobs returns errors other than 255.
    function check_bjobs_status_code {
        err_code=$1
        if [ "$err_code" -ne 0 ]; then
        if [ "$err_code" -eq 255 ]; then
            echo "bjobs returned error code 255, but we allow to continue .."
        else
            echo "bjobs failed with code $err_code"
            exit 1
        fi
        fi
    }
    bjobs 2> >(grep -v "No such file or directory") >/dev/null
    check_bjobs_status_code $?
    echo "LSF cluster availability:"
    set +x  # Avoid tracing thousands of lines of bjobs
    bjobs_states=$(bjobs -u all 2>/dev/null)
    check_bjobs_status_code $?
    pending_jobs=$(echo "$bjobs_states" | grep -c PEND)
    echo "--------------------------------------------------"
    echo "Running jobs: $(echo "$bjobs_states" | grep -c RUN)"
    echo "Pending jobs: $(echo $pending_jobs)"
    echo "--------------------------------------------------"
    echo $pending_jobs > pending_jobs_count
    set -x
    set -e
}

run_tests () {
    set -e
    if [[ "$CI_RUNNER_LABEL" == "azure" ]]; then
        #RUNNER_ROOT="/lustre1/users/f_scout_ci/egg_tests"
        echo "Skip running everest tutorial integration test on azure for now"
        return 0
    elif [[ "$CI_RUNNER_LABEL" == "onprem" ]]; then
        RUNNER_ROOT="/scratch/oompf/everest-integration-tests"
    else
        echo "Unsupported runner label: $CI_RUNNER_LABEL"
        return 1
    fi
    mkdir -p "$RUNNER_ROOT"
    run_path=$(mktemp -d -p "$RUNNER_ROOT")
    chmod ugo+rx "$run_path"
    cp -rf . "$run_path"/everest-tutorials
    pushd "$run_path"/everest-tutorials
    # Need to create a komodoenv on a network mapped drive for LSF etc.
    source "${_KOMODO_ROOT}"/"${_FULL_RELEASE_NAME}"/enable
    komodoenv --root "${_KOMODO_ROOT}" -r "${_FULL_RELEASE_NAME}" --no-update --force test-kenv
    source test-kenv/enable
    check_queue "$CI_RUNNER_LABEL"
    pip install --upgrade pip
    pip install .
    release_name=$(echo "$_FULL_RELEASE_NAME" | cut --delimiter=- --fields=1)
    set +e
    python -m pytest -svv tests | tee pytest-output
    if [[ "$?" -eq "1" ]]; then
        # The failure return code should be masked if this is due to pytest timing out,
        # then we assume that the compute cluster was too busy to fulfill the test.
        read -r pending_count < "pending_jobs_count"
        : ${GITHUB_OUTPUT:="github_output_default"}
        if grep -q "Failed: Timeout" pytest-output && [ "$pending_count" -gt 50 ]; then
            echo timeout_reason="probably too many pending jobs ($pending_count) on cluster" >> $GITHUB_OUTPUT
            exit 0
        else
            exit 1
        fi
    fi
    set -e
    # Clean up the temp folder removing folders older than 7 days
    find "$RUNNER_ROOT" -maxdepth 1 -mtime +7 -user f_scout_ci -type d -exec rm -r {} \;
}
