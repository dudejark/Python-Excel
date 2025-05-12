To run this project, first set the following variables:

export ACCOUNT_SID=""
export AUTH_TOKEN=""
export TWILIO_SANDBOX_NUMBER=""
export RECEIVER_WHATSAPP_NUMBER=""

or put these in an exports file,

```bash
pip3 -r requirements.txt
```
to activate the virtual environment 

```bash
source venv/bin/activate
```
to de-activate the virtual environment 

```bash
deactivate

```

```bash
source exports
```

```bash
python3 whatsapp_1.py
```