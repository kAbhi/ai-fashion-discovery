"use client";

import Link from "next/link";
import { useState } from "react";
import { Sparkles, Menu, X, ShoppingBag } from "lucide-react";

export function Navigation() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <Sparkles className="size-5" aria-hidden="true" />
            <span className="text-xl font-bold tracking-tight">Fashion Discovery</span>
          </Link>

          {/* Desktop navigation */}
          <div className="hidden md:flex items-center gap-8">
            <Link
              href="/"
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
            >
              Home
            </Link>
            <Link
              href="/occasions"
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
            >
              Occasions
            </Link>
            <Link
              href="/wishlist"
              className="relative text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
            >
              <ShoppingBag className="size-4" aria-hidden="true" />
              Wishlist
            </Link>
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 text-muted-foreground hover:text-foreground"
            aria-label="Toggle menu"
            aria-expanded={isOpen}
          >
            {isOpen ? <X className="size-5" /> : <Menu className="size-5" />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <div className="md:hidden bg-background border-b border-border p-4">
          <div className="space-y-4">
            <Link
              href="/"
              onClick={() => setIsOpen(false)}
              className="block text-sm font-medium text-foreground"
            >
              Home
            </Link>
            <Link
              href="/occasions"
              onClick={() => setIsOpen(false)}
              className="block text-sm font-medium text-foreground"
            >
              Occasions
            </Link>
            <Link
              href="/wishlist"
              onClick={() => setIsOpen(false)}
              className="block text-sm font-medium text-foreground"
            >
              Wishlist
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
}
