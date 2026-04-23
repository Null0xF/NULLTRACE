import sys
from cli import setup_cli
from core.engine import OSINTEngine
from core.deep_correlator import DeepCorrelator
from output.json_writer import JSONWriter
from output.csv_writer import CSVWriter
from output.graph_writer import GraphWriter
from core.banner import print_banner

def main():
    # Force utf-8 encoding for standard output if supported (Windows fix)
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    # Parse CLI arguments
    args = setup_cli()

    # Map short flags to command/target if used
    if args.short_user:
        args.command, args.target = "username", args.short_user
    elif args.short_email:
        args.command, args.target = "email", args.short_email
    elif args.short_domain:
        args.command, args.target = "domain", args.short_domain
    elif args.short_profile:
        args.command, args.target = "profile", args.short_profile

    if not args.command:
        print("[-] Error: You must specify a target. Use -h for help.")
        sys.exit(1)

    # Print the ASCII banner
    print_banner()

    # ── PRO MODE: Deep correlation ────────────────────────────────────────
    correlate = getattr(args, "correlate", False)
    graph     = getattr(args, "graph", False)

    if correlate:
        if args.command not in ("email", "e"):
            print("[-] --correlate is only supported with the 'email' command.")
            sys.exit(1)
        correlator = DeepCorrelator()
        results = correlator.run(args.target)
        # Wrap in standard structure for export
        export_data = {"query": args.target, "results": results}
    else:
        # ── Standard mode ─────────────────────────────────────────────
        engine = OSINTEngine()
        if args.command in ("profile", "p"):
            export_data = engine.run_profile(args.target)
        else:
            export_data = engine.run(args.command, args.target)

    # ── Output ────────────────────────────────────────────────────────────
    if args.format == "csv":
        CSVWriter.write(export_data)
    else:
        JSONWriter.write(export_data)

    if graph:
        GraphWriter.write(export_data, output_file="nulltrace_graph.html")

if __name__ == "__main__":
    main()

