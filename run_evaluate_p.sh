python -u evaluate_retrieved_passages_pop.py \
    --data ./../autodl-tmp/re_data/re_subnq/retrieved_dev_data_newpsgs_m2.json \
    --pop True \
    --l_dir ./../autodl-tmp/re_data/re_subnq/NQ-sub-open.subj.8.json \
    --levels 8 \
    --type subj \

python -u evaluate_retrieved_passages_pop.py \
    --data ./../autodl-tmp/re_data/re_subnq/retrieved_test_data_newpsgs_m2.json \
    --pop True \
    --l_dir ./../autodl-tmp/re_data/re_subnq/NQ-sub-open.subj.8.json \
    --levels 8 \
    --type subj \