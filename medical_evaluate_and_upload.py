import lm_eval
import json
import argparse
import os
from huggingface_hub import HfApi


def run_lm_eval(model, tasks, device, batch_size, log_samples):
    results = lm_eval.simple_evaluate(
        model="hf",
        model_args=f"pretrained={model}",
        tasks=tasks.split(","),
        device=device,
        batch_size=batch_size,
        log_samples=log_samples,
    )

    return results


def process_output(results):
    print("Processing results")

    rounded_results = {
        key: {k: round(v, 6) if isinstance(v, float) else v for k, v in value.items()}
        for key, value in results.get("results", {}).items()
    }

    modified_data = {
        "config": {
            "model_name": results.get("config", {}).get("model_args", "").replace('pretrained=', ''),
            "model_sha": results.get("config", {}).get("model_sha", ""),
            "model_dtype": str(results.get("config", {}).get("model_dtype", "")),
            "model_num_parameters": results.get("config", {}).get("model_num_parameters", ""),
        },
        "results": rounded_results,
    }

    modified_output_path = f'modified_results_{os.urandom(4).hex()}.json'
    print(f"Saving modified data to: {modified_output_path}")
    with open(modified_output_path, "w") as file:
        json.dump(modified_data, file, indent=2)

    api = HfApi()
    repo_id = "lion-ai/eskulap_medical_leaderboard_results"
    print(f"Uploading file: {modified_output_path} to Hugging Face repository: {repo_id}")
    api.upload_file(
        path_or_fileobj=modified_output_path,
        path_in_repo=f"{modified_data['config']['model_name'].split('/')[-1]}/{os.path.basename(modified_output_path)}",
        repo_id=repo_id,
        repo_type="dataset"

    )
    print("Results successfully uploaded to leaderboard.")


def main():
    parser = argparse.ArgumentParser(description="Run lm-eval and process its output.")
    parser.add_argument("--model", type=str, required=True, help="The name of the model to evaluate.")
    parser.add_argument("--tasks", type=str, required=False, default="medmcqa_pl,medical_mmlu_pl,pubmedqa_pl,lek_pl,med4qa_pl",
                        help="Tasks to run (e.g., 'medmcqa_pl,medical_mmlu_pl,pubmedqa_pl').")
    parser.add_argument("--device", type=str, default="0", help="Device to use for evaluation (e.g., 'cuda:0').")
    parser.add_argument("--batch_size", type=str, default=2, help="Batch size for evaluation. Write auto for automatic batch size.")
    parser.add_argument("--log_samples", action="store_true", help="Flag to log samples.")

    args = parser.parse_args()

    if not os.getenv("HF_TOKEN"):
        print("Authorization token not found in environment variables. Please set HF_TOKEN.")
        exit(1)

    results = run_lm_eval(
        model=args.model,
        tasks=args.tasks,
        device=args.device,
        batch_size=args.batch_size,
        log_samples=args.log_samples,
    )

    if results:
        process_output(results)


if __name__ == "__main__":
    main()