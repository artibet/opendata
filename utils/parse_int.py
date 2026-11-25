from utils import clean_str

def parse_int(value: str | None) -> int | None:
  cleaned = clean_str(value)
  if cleaned is None:
      return None
  try:
      return int(float(cleaned))
  except ValueError:
      return None