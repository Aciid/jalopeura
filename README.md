<p align="center" width="100%">
<img src="./assets/jalopeura2.png" alt="jalopeura" style="border:none; width: 20%; min-width: 300px; display: block; margin: auto;">
</p>

# Jalopeura: A Finnish fine-tune for LLaMA

This repository is intended to share information and resources on how to translate, measure performance and fine-tune Finnish translation of alpaca-lora.

## References

The project workflow is inspired by the many great LLM projects. Mentions [Alpaca Lora](https://github.com/tloen/alpaca-lora), [vigogne](https://github.com/bofenghuang/vigogne), [cabrita](https://github.com/22-hours/cabrita), [camoscio](https://github.com/teelinsan/camoscio)

## Data

Dataset is translated with ChatGPT in Finnish. Translation done by ChatGPT is not best on the market, but best given price ratio.
If you want to know more about how the dataset was built please see: [Stanford Alpaca](https://github.com/tatsu-lab/stanford_alpaca).
All 51,785 prompts from original alpaca-lora cleaned dataset are now translated, some prompts are missing due to resource exhaustion because of ratelimit reaching backoff maxinum. 

## Fine-tune

Finetuned model for LLaMA-7B using this translated model is available in HF. [aciidix/jalopeura-lora-7B](https://huggingface.co/aciidix/jalopeura-lora-7b).
