"use client";

import { useCallback, useEffect, useState } from "react";
import { CircleAlert, CircleCheck, Loader2, RefreshCw } from "lucide-react";

import { Button } from "@/components/ui/button";
import { fetchHealth, type HealthResult } from "@/services/health";

type State = { kind: "loading" } | HealthResult;

export function SystemStatus() {
  const [state, setState] = useState<State>({ kind: "loading" });

  const check = useCallback(async () => {
    setState({ kind: "loading" });
    setState(await fetchHealth());
  }, []);

  useEffect(() => {
    void check();
  }, [check]);

  return (
    <section
      aria-labelledby="system-status-heading"
      className="bg-card text-card-foreground w-full rounded-xl border p-5 shadow-sm"
    >
      <div className="flex items-center justify-between gap-4">
        <h2 id="system-status-heading" className="text-base font-semibold">
          System status
        </h2>
        <Button
          variant="outline"
          size="sm"
          onClick={() => void check()}
          disabled={state.kind === "loading"}
        >
          <RefreshCw aria-hidden="true" />
          Recheck
        </Button>
      </div>

      <div className="mt-4" role="status" aria-live="polite">
        {state.kind === "loading" && (
          <p className="text-muted-foreground flex items-center gap-2 text-sm">
            <Loader2 className="size-4 animate-spin" aria-hidden="true" />
            Checking backend…
          </p>
        )}

        {(state.kind === "ok" || state.kind === "degraded") && (
          <dl className="grid grid-cols-2 gap-y-2 text-sm">
            <dt className="text-muted-foreground">API</dt>
            <dd className="flex items-center gap-1.5 font-medium">
              <CircleCheck className="size-4 text-emerald-600" aria-hidden="true" />
              Reachable
            </dd>
            <dt className="text-muted-foreground">Database</dt>
            <dd className="flex items-center gap-1.5 font-medium">
              {state.data.database === "ok" ? (
                <CircleCheck className="size-4 text-emerald-600" aria-hidden="true" />
              ) : (
                <CircleAlert className="size-4 text-amber-600" aria-hidden="true" />
              )}
              {state.data.database === "ok" ? "Connected" : "Unavailable"}
            </dd>
            <dt className="text-muted-foreground">Environment</dt>
            <dd className="font-medium">{state.data.environment}</dd>
          </dl>
        )}

        {(state.kind === "unreachable" || state.kind === "misconfigured") && (
          <p className="text-destructive flex items-center gap-2 text-sm">
            <CircleAlert className="size-4" aria-hidden="true" />
            {state.message}
          </p>
        )}
      </div>
    </section>
  );
}
