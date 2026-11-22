from langchain.agents.middleware import PIIMiddleware

pii_middleware_email = PIIMiddleware(
    pii_type="email",
    strategy="mask",
    apply_to_input=False,
    apply_to_output=True
)
