"""CLI for Model Cascade Confidence Router."""
import argparse
import json
from .core import ModelCascadeRouter


def main():
    parser = argparse.ArgumentParser(description="Model Cascade Confidence Router CLI")
    parser.add_argument("--confidence", type=float, default=0.72, help="Draft model confidence")
    parser.add_argument("--text", default="It might be port 8080.", help="Draft output text")
    args = parser.parse_args()

    router = ModelCascadeRouter()
    print(json.dumps(router.evaluate_draft(args.text, confidence=args.confidence), indent=2))


if __name__ == "__main__":
    main()
