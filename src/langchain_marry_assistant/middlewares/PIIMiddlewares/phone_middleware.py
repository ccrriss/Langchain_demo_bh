from langchain.agents.middleware import PIIMiddleware

pii_middleware_phone = PIIMiddleware(
    pii_type="phone_number",
    strategy="redact",
    detector=r"(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{4}",
    apply_to_output=True
)