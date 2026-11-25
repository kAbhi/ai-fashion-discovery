import { Sparkles } from "lucide-react";

import { SystemStatus } from "@/components/system-status";

export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-dvh w-full max-w-md flex-col items-center justify-center gap-8 px-5 py-12 sm:max-w-lg">
      <header className="flex flex-col items-center gap-3 text-center">
        <Sparkles className="size-8" aria-hidden="true" />
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Fashion Discovery</h1>
        <p className="text-muted-foreground text-sm">
          Occasion-first fashion discovery. The shopping experience is under construction.
        </p>
      </header>
      <SystemStatus />
    </main>
  );
}
