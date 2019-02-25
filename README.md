# sort-sort-of-clevr

This is repository for sort-sort-of-clevr dataset creation. This dataset follows [sort-of-clevr](https://arxiv.org/abs/1706.01427) dataset but a few points are different (e.g. captions, dataset settings..).

## Requirements

- [gizeh](https://github.com/Zulko/gizeh)
- scipy
- (Optional) [skipthoughts](https://github.com/ryankiros/skip-thoughts)

## (Optional) Embed sentences with skipthoughts

Run `python source/prepare_dataset.py` will do this thing. Before run this code, you must replace some paths in this file such as `dataset_dir`.
