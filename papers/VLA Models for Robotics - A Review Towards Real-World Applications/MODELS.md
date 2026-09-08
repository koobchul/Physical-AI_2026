This document summarizes the representative models introduced in the survey.

```text
Representative Works
├──  
│   ├── 
│   └── 
│
├──  
│   ├── 
│   └── 
│
└── 
    ├── 
    ├── 
    └── 
```

# CNN-based end-to-end architectures

### CLIPort (Shridhar et al., 2022)

- earlist models to integrate CLIP for extracting visual and linguistic features
- combines these modalities with the Transporter Network 
- learn object manipulation tasks in an end-to-end manner
- demonstraed the feasibility of jointly training VLA by leveraging CLIP as a pre-trained VLM
- Limitations: CNN, MLP face challenges in unifying diverse modalities and also struggle to scale effectively

# Transformer-based sequence models 

### Gato (Scott et al., 2022)

- generalist agent and precursor to the Robotics Transformer (RT) series
- using a single tranformer model 
    - performs a wide range of tasks
         - text chatting
         - visual question answering
         - image captioning
         - game play
         - robot control 
- tokenizes languague instructions using SentencePice
- encode images using Vision Transformer (ViT)
- decoder-only transformer is then used to autoregressively generate actions based on the combined input sequence

### Vima (Jiang et al., 2022)

- encoder-decoder transformer model that enables robots to follow general task instructions provided through a combination of text and goal images
- objects are first detected using Mask R-CNN
- after which each detected object's image is tokenized using ViT
- Bounding box cooradinates are separately embedded as tokens 
- textual instructions are tokenized using the T5 tokenizer

# Unified real-world policies with pre-trained VLMs

### RT-1 (Anthony et al., 2023)

- processes a sequence of images using EfficientNet
- performs FiLM conditioning with language features encoded by Univer Sentence Encoder (USE)
- enable early fusion of visual and linguistic modalities
- extracted tokens are compressed via TokenLearner 
- then passed through a decoder-only transformer 
- outputs discretized action tokens nonautoregressively 

>regarded as the first VLA that unifies a broad range of robotic tasks

### RT-2 (Brohan et al., 2023)

- builds on a VLM backbone such as PaLM-E or PaLI-X
- pre-trained on large-scale internet data
- jointly fine-tuned on both internet-scale vision-language tasks and robotic data from RT-1
- result in strong generalization to novel environments

> become the standard architecture for VLAs

### RT-X (O'Neill et al., 2024)

- demonstrate that training on datasets collected from multiple robots
- enable the development of more general-purpose VLAs

### RT series

#### RT-Sketch

- input: sketch images

#### RT-Trajectoy

- input: motion trajectories

#### RT-H

> introducing a hierarchical policy structure

- incorporates a high-level policy that predicts and intermedite representation known as language motion 
- low-level policy that generates ations based on it
- by modifying the input prompt\
the model can flexibly alternate between genearting high-level and low-leve policies
- domonstrages improved performance in long-horizon tasks

#### Sara-RT
#### AutoRT

### OpenVLA (Kim et al., 2024)

- open-source VLA framework that closely mirrors the architecture of RT-2
- leveraging a pre-trained VLM as its backbone
- employs Prismatic VLM
- based on LLaMa 2 (7B)
- encodes image inputs using DINOv2 and SigLIP
- through full fine-tuning on the Open-X Embodiment (OXE) dataseet, OpenVLA outperforms both RT-2 and Octo

> emerged as a mainstream architecture for VLA

# Diffusion policy

### Octo (Dibya et al., 2024)

- gained attention for its fully open-source implementation
- supports filxible goal specification 
- can include a language instruction and a goal image, processed by a T5 encoder and a CNN
- input: CNN to encode images 
- lightweight multilayer preceptron (MLP) to embed proprioceptive signals
- all tokens are concatenated into a single sequence, augmented with modality-specific learnable tokens, and passed into a transformer
- diffusion policy generates continuous actions conditioned on the output readout tokens

>first VLA to leverage Diffusion Policy

# Diffusion transformer architectures

### RDT-1B (Liu et al., 2025)

- proposed as a large-scale diffusion transformer for robotics
- backbone: Diffusion Transformer(DiT) 
- intergrage the diffusion process directily into the transformer decoder to generate actions
- language inputs are tokeized using the T5 encoder
- visual inputs are encoded using SigLIP
- diffusion model is then trained using a diffusion transformer with cross-attention 
- conditioned on both visual and textual tokens
- Alternating Condition Injection is proposed to facilitate multimodal conditioning and avoid overfitting
     - image and text tokens are alternately used as queries at each transformer layer

> proposed as a large-scale diffusion transformer for robotics

# Flow matching policy architectures

### π0

- builds on PaliGemma 
- introduce a custom action output module
- action expert enable a multimodal model to handle both discrete and continuous data
- leverage flow-matching to generate actions to generate actions at rates up to 50Hz
- receive proprioceptive input from the robot
- readout token from the transformer
- producing actions through a reverse diffusion process

> outputs entire action chunks in parallel, enabling smooth and consistent real-time control

# Latent action learning from video 

### LAPA (Ye et al., 2025)

- leverage unlabeled video data for pre-training to learn latent actions for use in VLA model
- enable policies to effectively utilize human demonstrations
- make them robust to changes in embodiment and well-suited for real-world deployment
- apply patch embeddings, spatial transformer, and casual temporal transformer to images then computes their difference
- applied VQ-VAE to this difference
- entire network is trained jointly, forming a Latent Quantization Network 
- Build on LWN-Chat-1M(7B)
    - visionand text encoders are kept frozen
    - resulting readout token is processed through an MLP trained to zredict z_t
- only the MLP component is replaced by a seperate network trained to directly output robot control commands

# Hierarchical policy architectures

### RT-H (Belkhale et al., 2024)

- high-level controller that predicts intermediate "language motion" plans
- switch between sequences, improving preformancs in long-horizon, multi-step tasks

### π0.5 (Brian et al., 2025)

- comibne high-level action token generation with low-level controller trained via flow matching
- pre-training aligns symbolic actions woth language
- post-training enseures smooth execution via continuous action decoding 

### GROOT N1 (Nvidia et al., 2025)

> integrage multiple elements

- unified into a multi-stage policy that generalizes across robots and tasks
    - LAPA : altent actions from LAPA
    - RDT-1B : diffusion based generation 
    - π0 : flow-matching controllers

# A. SENSORIMOTER MODEL 

## Transformer + Discrete Action Token

- represent both image and language as tokens
- fed into a transformer to predict the next action 
- include models that use CLS tokens
- generate continuous actions through and MLP
- Representative examples
    - VIMA 
        - employ an encoder-decoder transformer conditioned on diverse task modalities
    - Gato
        - uses a decoder-only transformer that autoregressively processes all tokens in a single sequence
    - tokenize multiple modalitiees using language tokenizers, vision transformers, MLPs, and other components
    - output discretized actions (binned values)
    
### RT-1 (Brohan et al., 2023)

- compressing inputs using TokenLearner
- employing a decoder-only transformer to predict all action tokens non-autoregressively
- 48 tokens are fed into the transformer
- final 11 tokens are extracted as action outputs
- Representative examples 
    - MOO
    - RT-Sketch
    - RT-Trajectory
    - Robocat
    - RoboFlamingo

## Transformer + Diffusion Action Head

- Representataive examples
    - Octo
        - process image and language tokens as a single sequence through a transformer
        - applies a diffusion action head conditioned on the readout token 
    - NoMAD
        - replace the language input with a goal image
        - compress the transformer output via average pooling
        - use the resulting vector to condition the diffusion model
    - TinyVLA
    - RoboBERT
    - VidBot

## Diffusion Transformer

- integrates the transformer and diffusion action head
- Representative examples
    - RDT-1B
        - generate a sequence of action tokens via cross-attention with a vision and language query
        - mapped to executable robot actions through MLP
        - Large Behavior Models (LBMs) apopt the diffusion transformer architecture and emphasize the importance of large-scale and diverse pre-training
    - StructDiffusion 
    - MDT
    - DexGraspVLA
    - UVA
    - FP3
    - PPL
    - PPI
    - Dita

## VLM + Discrete Action Token 

- Representative examples
    - RT-2 
        - backbone: large-scale VLMs (PalM-E, PaLI-X)
            - processes image and language tokens as input and outputs the next action as discrete tokens
    - LEO
    - GR-1
    - RT-H
    - RoboMamba
    - QUAR-VLA 
    - OpenVLA
    - LLARA
    - ECoT
    - 3D-VLA
    - RoboUniView
    - CoVLA

## VLM + Diffusion Action Head

- Representative examples 
    - Diffusion-VLA
    - DexVLA
    - ChatVLA
    - ObjectVLA
    - GO-1 (AgiBot World Colosseo)
    - PointVLA
    - MoLe-VLA
    - Fis-VLA
    - CronusVLA
    - HybridVLA
        - autoregressively generate discrete tokens as well as use a diffusion action head to generate continuous actions within a single model

## VLM + Flow Matching Action Head

- replace the diffusion model with a flow matching action head
- imporve real-time responsiveness while maintaining smooth, continuous control
- Representative examples
    - π0
        - baesd on PaliGemma
        - achieves control rate of up to 50 Hz
    - GraspVLA
    - OneTwoVLA
    - Hume
    - SwitchVLA
    - π0.5
        - supporting both discrete tokens and flow matching within a unified framework

## VLM + Diffusion Transformer

- combine a VLM with a diffusion transformer
- Representative examples
    - GROOT N1
        - applies cross-attention from the diffusion transformer to VLM tokens and generates continuous actions via flow matching 
    - CogACT
    - TrackVLA
    - SmolVLA
    - MinD

# B. WORLD MODEL 