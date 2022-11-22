import torch
from transformers import pipeline, AutoModelWithLMHead, AutoModelForSeq2SeqLM, AutoModelForMaskedLM, \
    AutoModelForCausalLM
from transformers import FSMTForConditionalGeneration, FSMTTokenizer
import os
from sentence_transformers import SentenceTransformer, util
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from mods.mainTool import MainTool, FileHandler
from Style import Style
from huggingface_hub import HfFolder
from huggingface_hub import InferenceApi
import time


class Tools(MainTool, FileHandler):

    def __init__(self, app=None):
        self.version = "0.0.1"
        self.name = "isaa"
        self.logs = app.logs_ if app else None
        self.color = "VIOLET2"
        self.inference = InferenceApi
        self.config = {}
        self.isaa_instance = {"Stf": {},
                              "DiA": {}}
        self.keys = {
            "KEY": "key~~~~~~~",
            "Config": "config~~~~"
        }
        self.tools = {
            "all": [["Version", "Shows current Version"],
                    ["Run", "Starts Inference"],
                    ["add_api_key", "Adds API Key"],
                    ["login", "Login"],
                    ["new-sug", "Add New Question or Class to Config"],
                    ["run-sug", "Run Huggingface Pipeline"],
                    ["info", "Show Config"],
                    ],
            "name": "isaa",
            "Version": self.show_version,
            "Run": self.ask_Bloom,
            "add_api_key": self.add_api_key,
            "login": self.login,
            "new-sug": self.new_sub_grop,
            "run-sug": self.run_sug,
            "info": self.info,
        }

        FileHandler.__init__(self, "issa.config", app.id if app else __name__)
        MainTool.__init__(self, load=self.on_start, v=self.version, tool=self.tools,
                          name=self.name, logs=self.logs, color=self.color, on_exit=self.on_exit)

    def show_version(self):
        self.print("Version: ", self.version)

    def on_start(self):
        self.open_l_file_handler()
        self.load_file_handler()
        config = self.get_file_handler(self.keys["Config"])
        if config is not None:
            self.config = eval(config)

            start_time = time.time()
            stf = "all-MiniLM-L6-v2"
            dia = "microsoft/DialoGPT-large"
            if "ai-config" in self.config:
                ai_config = self.config["ai-config"]
                stf = ai_config["SentenceTransformer"]
                dia = ai_config["Dialog"]
            else:
                self.config["ai-config"] = {"SentenceTransformer": stf, "Dialog": dia}
            start_time_dia = time.time()
            self.add_tmk(["", "DiA", dia, "wmhtkz"])
            process_time_dia = time.time() - start_time_dia
            start_time_stf = time.time()
            self.add_tmk(["", "Stf", stf, "stf"])
            process_time_stf = time.time() - start_time_stf
            process_time_total = time.time() - start_time

            self.print(
                f"Processing time :\n\tTotal {process_time_total:.2f} seconds\n\tDia {process_time_dia:.2f} seconds\n\t"
                f"Stf {process_time_stf:.2f} seconds")

    def add_tmk(self, command):
        if len(command) < 2:
            return "invalid"
        ap = command[1]
        name = command[2]
        mode = command[3]

        ai_c = {"tokenizer": None, "model": None}

        self.print(name)

        if "tkz" in mode:
            ai_c["tokenizer"] = AutoTokenizer.from_pretrained(name, padding_side='left')

        if "wmh" in mode:
            ai_c["model"] = AutoModelWithLMHead.from_pretrained(name, from_tf=False)

        if "s2s" in mode:
            ai_c["model"] = AutoModelForSeq2SeqLM.from_pretrained(name, from_tf=False)

        if "msk" in mode:
            ai_c["model"] = AutoModelForMaskedLM.from_pretrained(name, from_tf=False)

        if "ca" in mode:
            ai_c["model"] = AutoModelForCausalLM.from_pretrained(name, from_tf=False)

        if "stf" in mode:
            ai_c["model"] = SentenceTransformer(name)

        self.isaa_instance[ap] = ai_c

    def on_exit(self):
        self.add_to_save_file_handler(self.keys["Config"], str(self.config))
        self.open_s_file_handler()
        self.save_file_handler()
        self.file_handler_storage.close()

    def add_api_key(self):
        key = input("~")
        if key == "":
            self.print(Style.RED("Error: Invalid API key"))
            return
        self.add_to_save_file_handler(self.keys["KEY"], key)

    def login(self):
        api_key = self.get_file_handler(self.keys["KEY"])
        if api_key is not None:
            self.print(api_key)
            os.system("huggingface-cli login")
            self.inference = InferenceApi("bigscience/bloom", token=HfFolder.get_token())
            return
        self.print(Style.RED("Please enter your API key here:"))
        self.add_api_key()

    def ask_Bloom(self, _input):
        des = _input[1:]
        s = ""
        for i in des:
            s += str(i) + " "
        resp = infer(s, inference=self.inference)
        self.print(resp)

    def new_sub_grop(self, command):
        if len(command) <= 3:
            return "invalid command length [sug:name type:question:class:ed:de data:{question:Um-wie-viel-uhr, " \
                   "class:auto-katze-maus, de-ed:-}] "
        self.config[command[1]] = {"t": command[2], "data": command[3].replace("-", " "), "version": self.version}

    def info(self):
        self.print(self.config)
        return self.config

    def run_sug(self, command):
        name = command[1]
        data = command[2].replace('-', ' ')
        sug = self.config[name]
        t_ype = sug["t"]
        try:
            if t_ype == "ed":
                return pipeline_s("translation_en_to_de", data)
            elif sug["t"] == "de":
                return translation_ger_to_en(data)
            elif t_ype == "class":
                return pipeline_s('text-classification', data)
            elif t_ype == "question":
                return pipeline_q('question-answering', sug["data"], data)
            elif t_ype == "q-t-d-e-d":
                data = translation_ger_to_en(data)
                data = pipeline_q('question-answering', sug["data"], data)['answer']
                return pipeline_s("translation_en_to_de", data)
            elif t_ype == "stf":
                return pipeline_stf(data, sug["data"], self.isaa_instance['Stf']['model'])
            elif t_ype == "talk":
                res, sug["data"] = pipeline_talk(data, self.isaa_instance['DiA']['model'],
                                                 self.isaa_instance['DiA']['tokenizer'], sug["data"])
                return res
        except Exception as e:
            self.print(Style.RED(str(e)))
        return data


# install pytorch ->
# conda install pytorch torchvision torchaudio cpuonly -c pytorch
# pip3 install torch torchvision torchaudio
pipeline_arr = [
    # 'audio-classification',
    # 'automatic-speech-recognition',
    # 'conversational',
    # 'depth-estimation',
    # 'document-question-answering',
    # 'feature-extraction',
    # 'fill-mask',
    # 'image-classification',
    # 'image-segmentation',
    # 'image-to-text',
    # 'ner',
    # 'object-detection',
    'question-answering',
    # 'sentiment-analysis',
    # 'summarization',
    # 'table-question-answering',
    'text-classification',
    # 'text-generation',
    # 'text2text-generation',
    # 'token-classification',
    # 'translation',
    # 'visual-question-answering',
    # 'vqa',
    # 'zero-shot-classification',
    # 'zero-shot-image-classification',
    # 'zero-shot-object-detection',
    'translation_en_to_de'
]


# result = question_answerer(question="What is extractive question answering?", context=context)
def pipeline_c(data):
    model = AutoModelForSequenceClassification.from_pretrained("palakagl/bert_TextClassification",
                                                               use_auth_token=True)
    tokenizer = AutoTokenizer.from_pretrained("palakagl/bert_TextClassification", use_auth_token=True)
    inputs = tokenizer(data, return_tensors="pt")
    m = model(**inputs)
    print(m)
    return m


def pipeline_s(name, string):
    pipe = pipeline(name, return_all_scores=True)
    return pipe(string)


def pipeline_q(name, question, context):
    pipe = pipeline(name)
    qa = {
        'question': question,
        'context': context
    }
    return pipe(qa)


def translation_ger_to_en(input):
    mname = "facebook/wmt19-de-en"
    tokenizer = FSMTTokenizer.from_pretrained(mname)
    model = FSMTForConditionalGeneration.from_pretrained(mname)
    input_ids = tokenizer.encode(input, return_tensors="pt")
    outputs = model.generate(input_ids)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def infer(prompt,
          max_length=32,
          top_k=0,
          num_beams=0,
          no_repeat_ngram_size=2,
          top_p=0.9,
          seed=42,
          temperature=0.7,
          greedy_decoding=False,
          return_full_text=False, inference=InferenceApi):
    top_k = None if top_k == 0 else top_k
    do_sample = False if num_beams > 0 else not greedy_decoding
    num_beams = None if (greedy_decoding or num_beams == 0) else num_beams
    no_repeat_ngram_size = None if num_beams is None else no_repeat_ngram_size
    top_p = None if num_beams else top_p
    early_stopping = None if num_beams is None else num_beams > 0

    params = {
        "max_new_tokens": max_length,
        "top_k": top_k,
        "top_p": top_p,
        "temperature": temperature,
        "do_sample": do_sample,
        "seed": seed,
        "early_stopping": early_stopping,
        "no_repeat_ngram_size": no_repeat_ngram_size,
        "num_beams": num_beams,
        "return_full_text": return_full_text
    }

    s = time.time()
    response = inference(prompt, params=params)
    # print(response)
    print(f"Process took {time.time() - s: .2f} seconds to complete")
    # print(f"Processing time was {proc_time} seconds")
    return response


def pipeline_talk(user_input, model, tokenizer, chat_history_ids):
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if len(
        chat_history_ids) > 9999 else new_user_input_ids
    # generated a response while limiting the total chat history to 1000 tokens,
    chat_history_ids = model.generate(
        bot_input_ids, max_length=1500,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,
        do_sample=True,
        top_k=180,
        top_p=0.2,
        temperature=0.99,
    )
    res = "Isaa: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True,
                                             padding_side='left'))
    # pretty print last ouput tokens from bot
    return res, chat_history_ids


def pipeline_stf(s1, s2, model):
    # 'all-MiniLM-L6-v2')
    embeddings1 = model.encode(s1, convert_to_tensor=True, show_progress_bar=True)
    embeddings2 = model.encode(s2, convert_to_tensor=True, show_progress_bar=True)
    cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)

    max_ = []
    m = 0
    for i, v in enumerate(s1):
        for j, b in enumerate(s2):
            c = float(cosine_scores[i][j])
            if c > m:
                m = c
                max_ = [v, b, c]
            print(f"v: {v} ,b: {b} ,Score: {float(cosine_scores[i][j]):.4f}")

    return max_

# "What time is the appointment?"
# "Appointment location?"
