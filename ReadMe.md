# EmotionTool (E.T.)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.11244222.svg)](https://doi.org/10.5281/zenodo.11244222)

E.T. is a small coding helper for the Children's Emotion Vocabulary Vignettes Test (CEVVT; Streubel et al., 2020). The program structure is influenced by the great work of Barchard et al. (2010).

## Prerequisites

Before running the program, ensure you have completed the following steps:

1. Create `.csv` wordlists in the "lists" folder:
   - `emotion_words.csv`
   - `modifier.csv`
   - `negation.csv`
2. Place the input file in the "in" folder.
3. Create a folder called "out".
4. Edit `settings.py` to suit your needs.

## Running the Program

You can start E.T. by running `main.py`. If you have Python installed, execute the following command in your terminal or cmd:

```
python main.py
```

If Python is not installed, you can download and install it from [here](https://www.python.org). We also provide a Windows batch file, `start.cmd`, to run E.T. with a portable version of Python. For a detailed description of the installation and labeling process, refer to `CEVVT_Coding_with_E.T1.0.pdf`.

## Example Files

We provide example input lists and input files, which are already in the "lists" and "in" folders.

## Citation

If you use E.T. in your research, please cite the following works:

- Barchard, K. A., Bajgar, J., Leaf, D. E., & Lane, R. (2010). Computer scoring of the Levels of Emotional Awareness Scale. *Behavior Research Methods, 42*, 586-595. doi: [10.3758/BRM.42.2.586](https://doi.org/10.3758/BRM.42.2.586)
- Streubel, B., Gunzenhauser, C., Grosse, G., & Saalbach, H. (2020). Emotion-specific vocabulary and its contribution to emotion understanding in 4-to 9-year-old children. *Journal of Experimental Child Psychology, 193*, 104790. doi: [10.1016/j.jecp.2019.104790](https://doi.org/10.1016/j.jecp.2019.104790)
