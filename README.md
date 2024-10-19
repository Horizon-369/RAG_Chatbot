# PDF Chatbot

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Examples](#examples)
7. [Troubleshooting](#troubleshooting)
8. [Contributing](#contributing)
9. [License](#license)

## Introduction

PDF Chatbot is an innovative tool built on Retrieval-Augmented Generation (RAG), enabling users to interact with the content of PDF documents through a dynamic chat interface. By leveraging cutting-edge natural language processing (NLP) and retrieval mechanisms, the chatbot combines the power of language models with vector databases to provide accurate, context-aware responses. It retrieves relevant information from the uploaded PDF and generates coherent answers to user queries, making it a highly efficient tool for research, study, and seamless information retrieval. This approach ensures both precision and fluency, transforming the way users interact with documents.

## Features

- Upload and process PDF documents
- Chat interface for asking questions about the PDF content
- Support for multi-query input (multiple questions at once)
- Integration with Cohere for natural language processing
- Utilizes Pinecone for efficient vector search
- User-friendly Gradio interface

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.7+
- pip (Python package manager)
- A Cohere API key
- A Pinecone API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Horizon-369/RAG_Chatbot.git
   cd RAG_Chatbot
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file in the project root and add your API keys:
   ```
   COHERE_API_KEY=your_cohere_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   ```

## Usage

### Locally

1. Run the application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal.

3. Upload a PDF file using the "Upload PDF" button.

4. Click "Process PDF" to extract and index the content.

5. Use the chat interface to ask questions about the PDF content.

### On Huggging Face Space

https://huggingface.co/spaces/Kshitij-369/RAG_Chatbot

## Examples

Here are some example interactions with the PDF Chatbot (with Health Nutrition PDF):

1. Single query:
   
   User: "What are the causes of type 2 diabetes?"
   
   Bot:
   
       To see how the rise in obesity in this country is paralleled by the rise in Type
       2 diabetes, review this report by the CDC.
       https://www.cdc.gov/diabetes/statistics/slides/ maps_diabetesobesity_trends.pdf 
       What is the causal relationship between overnutrition and Type 2 diabetes?The
       prevailing theory is that the overconsumption of high-fat and high-sugar foods
       causes changes in muscle, fat, and liver cells that leads to a diminished
       response from the pancreatic hormone insulin. These cells are called “insulin-
       resistant.”Insulin is released after a meal and instructs the liver and other
       tissues to take up glucose and fatty acids that are circulating in the blood.
       When cells are resistant to insulin they do not take up enough glucose and fatty
       acids, so glucose and fatty acids remain at high concentrations in the blood.
       The chronic elevation of glucose and fatty acids in the blood also causes damage
       to other tissues over time, so that people who have Type 2 diabetes are at
       increased risk for cardiovascular disease, kidney disease, nerve damage, and eye
       disease. The Endocrine System | 107

3. Multiple queries:
   User: "What is the importance of hydration for physical performance?", "What role does fibre play in digestion?"

   Bot:
   
        Result of 1st query:
        Image by Allison Calabrese / CC BY 4.0 Water and Electrolyte Needs UNIVERSITY OF
        HAWAI‘I AT MĀNOA FOOD SCIENCE AND HUMAN NUTRITION PROGRAM AND HUMAN NUTRITION
        PROGRAM During exercise, being appropriately hydrated contributes to
        performance. Water is needed to cool the body, transport oxygen and nutrients,
        and remove waste products from the muscles. Water needs are increased during
        exercise due to the extra water losses through evaporation and sweat.
        Dehydration can occur when there is inadequate water levels in the body and can
        be very hazardous to the health of an individual. As the severity of dehydration
        increases, the exercise performance of an individual will begin to decline (see
        Figure 16.9 “Dehydration Effect on Exercise Performance”). It is important to
        continue to consume water before, during and after exercise to avoid dehydration
        as much as possible. Figure 16.9 Dehydration Effect on Exercise Performance
        During exercise, thirst is not a reliable short term indicator of the body’s
        needs as it typically is not enough to replace the water loss. Even with the
        constant replenishing of water throughout an 972 | Water and Electrolyte Needs

        Result of 2nd query:
        Image by Allison Calabrese / CC BY 4.0 fiber intake because of what the
        breakdown products of the fiber do for the colon. The bacterial breakdown of
        fiber in the large intestine releases short-chain fatty acids. These molecules
        have been found to nourish colonic cells, inhibit colonic inflammation, and
        stimulate the immune system (thereby providing protection of the colon from
        harmful substances). Additionally, the bacterial indigestible fiber, mostly
        insoluble, increases stool bulk and softness increasing transit time in the
        large intestine and facilitating feces elimination. One phenomenon of consuming
        foods high in fiber is increased gas, since the byproducts of bacterial
        digestion of fiber are gases. Figure 18.2 Diverticulitis: A Disease of Fiber
        Deficiency Some studies have found a link between high dietary-fiber intake and
        a decreased risk for colon cancer. However an analysis of 1086 | Nutrition,
        Health and Disease

   

5. Specific content questions:
   User: "What is the RDI for protein per day?"

   Bot:

        Proteins, Diet, and Personal Choices UNIVERSITY OF HAWAI‘I AT MĀNOA FOOD SCIENCE
        AND HUMAN NUTRITION PROGRAM AND HUMAN NUTRITION PROGRAM We have discussed what
        proteins are, how they are made, how they are digested and absorbed, the many
        functions of proteins in the body, and the consequences of having too little or
        too much protein in the diet. This section will provide you with information on
        how to determine the recommended amount of protein for you, and your many
        choices in designing an optimal diet with high-quality protein sources. How Much
        Protein Does a Person Need in Their Diet? The recommendations set by the IOM for
        the Recommended Daily Allowance (RDA) and AMDR for protein for different age
        groups are listed in Table 6.2 “Dietary Reference Intakes for Protein”. A
        Tolerable Upper Intake Limit for protein has not been set, but it is recommended
        that you do not exceed the upper end of the AMDR. Table 6.2 Dietary Reference
        Intakes for Protein Proteins, Diet, and Personal Choices | 409
   

## Troubleshooting

- If you're not getting responses, make sure you've uploaded and processed a PDF first.
- Check that your Cohere and Pinecone API keys are correctly set in the `.env` file.
- Ensure that the Pinecone index is properly created and populated with the PDF content.

## Contributing

Contributions to the PDF Chatbot project are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## License

This project uses the following license: [MIT License](https://opensource.org/licenses/MIT).
