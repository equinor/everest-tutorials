run_tests () {
    set -e
    if [[ "$CI_RUNNER_LABEL" == "azure" ]]; then
        echo "Skip running everest tutorial integration test on azure for now"
        return 0
    elif [[ "$CI_RUNNER_LABEL" == "onprem" ]]; then
        RUNNER_ROOT="/scratch/oompf/everest-tutorials-tests"
    else
        echo "Unsupported runner label: $CI_RUNNER_LABEL"
        return 1
    fi

    # Create a temp folder and copy the repo there
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

    # Install the package
    pip install --upgrade pip
    pip install .
    release_name=$(echo "$_FULL_RELEASE_NAME" | cut --delimiter=- --fields=1)
    set +o errexit

    # Run the tests
    python -m pytest -vv -k "test_well_trajectory_simulation" tests
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
    set -o errexit

    # Clean up the temp folder removing folders older than 7 days
    find "$RUNNER_ROOT" -maxdepth 1 -mtime +7 -user f_scout_ci -type d -exec rm -r {} \;
}
