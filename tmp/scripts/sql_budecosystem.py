import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("budecosystem/sql-millennials-13b")
model = AutoModelForCausalLM.from_pretrained("budecosystem/sql-millennials-13b")

prompt  = "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. "
prompt += "USER: Create SQL query for the given table schema and question ASSISTANT:"
prompt += """
    create table invoices
    (
        id           int auto_increment primary key,
        order_id     int                           null,
        invoice_date datetime                      null,
        due_date     datetime                      null,
        tax          decimal(19, 4) default 0.0000 null,
        shipping     decimal(19, 4) default 0.0000 null,
        amount_due   decimal(19, 4) default 0.0000 null
    )
        charset = utf8mb3;
    
    create index fk_invoices_orders1_idx
        on invoices (order_id);
    
    create index id
        on invoices (id);
    
    create index id_2
        on invoices (id);
    
    
    """

inputs = tokenizer(prompt, return_tensors="pt")
sample = model.generate(**inputs, max_length=128)
print(tokenizer.decode(sample[0]))