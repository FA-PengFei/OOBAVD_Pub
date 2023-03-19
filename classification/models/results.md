## Model Results

| Model                     | Accuracy | Fixed |
| ------------------------- | -------- | ----- |
| Byteplot_resnet50         | 0.9617   | \*    |
| Byteplot_dct_resnet50     | 0.9121   |
| Byteplot_doc&pe_resnet50  | 0.9540   | \*    |
| Byteplot_doc_resnet50     | 0.9294   | \*    |
| Byteplot_doc&pe_resnet101 | 0.9563   | \*    |
| Byteplot_resnset101       | 0.9563   | \*    |

Getting the average of the two models (Doc & PE), it gets an average of 0.9455, compared to 0.9540 when merging two models into one.

Comparing the resnet50 model with resnet101, the differences seem to be within margin of error, with only a 0.25% increase in performance
