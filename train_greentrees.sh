#!/usr/bin/env bash

list_of_plots=(299)
# list_of_plots=(54 66 70 82 87 91 92 123 128 137 138 139 144 246 248 250 289 292 299 323 325 326 327 328 329 359 381)
# list_of_plots=(92 123 128 137 138 139 144 246 248 250 289 292 299 323 325 326 327 328 329 359 381)

for plot_id in ${list_of_plots[@]}; do
    # python downscale.py /workspace/GreenTrees/Plot"$plot_id"/images 2
    python train.py --config-name apps/colmap_3dgut_mcmc.yaml \
    path=/home/radagon/Documents/pipeline/outputs/greentree \
    out_dir=runs experiment_name=greentrees_final \
    export_ply.enabled=true test_last=false \
    export_ingp.enabled=false val_frequency=999999 \
    optimizer.type=selective_adam

    # path=/workspace/GreenTrees/Plot"$plot_id" \


done