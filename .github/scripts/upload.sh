#!/bin/bash

echo "Release Tag Name: $1"

gh release upload $1 everest-tutorials-egg.tar.gz
gh release upload $1 everest-tutorials-drogon.tar.gz
gh release upload $1 everest-tutorials-drogon-control_sens.tar.gz
gh release upload $1 everest-tutorials-drogon-multi_objective.tar.gz
gh release upload $1 everest-tutorials-drogon-well_order.tar.gz
gh release upload $1 everest-tutorials-drogon-well_rate.tar.gz
gh release upload $1 everest-tutorials-drogon-well_selection.tar.gz
gh release upload $1 everest-tutorials-drogon-well_swap.tar.gz
gh release upload $1 everest-tutorials-drogon-well_trajectory.tar.gz
