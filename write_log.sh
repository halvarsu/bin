echo -n date,jobid,program,commit,what,system,supercell,ecp,pbc?,name,cluster,
echo -n input path,output path,gpus used,nodes
echo
echo -n $(date +%d/%m/%y),
echo -n $SLURM_JOB_ID,
echo -n $PROGRAM,
echo -n $(git -C $FERMINET_DIR rev-parse HEAD),
echo -n , # what
echo -n , # system
echo -n , # supercell
echo -n , # ecp
echo -n , # pbc?
echo -n $SLURM_JOB_NAME, # name
echo -n $(hostname), # node
echo -n $INPUT_PATH, # input path
echo -n , # output path
echo -n $SLURM_GPUS, # gpus used
echo -n $SLURM_NNODES, # nodes
echo
