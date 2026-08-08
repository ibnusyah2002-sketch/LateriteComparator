"use client";

import Link from "next/link";
import { History, Home, Settings } from "lucide-react";
import { usePathname } from "next/navigation";

const navItems = [
  {
    label: "Scanner",
    href: "/",
    icon: Home,
  },
  {
    label: "History",
    href: "/history",
    icon: History,
  },
  {
    label: "Settings",
    href: "/settings",
    icon: Settings,
  },
];

export function BottomNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-4 left-1/2 z-50 w-[calc(100%-2rem)] max-w-[390px] -translate-x-1/2">
      <div className="grid grid-cols-3 rounded-full border border-white/10 bg-[#131816]/95 p-1.5 shadow-2xl backdrop-blur">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive =
            item.href === "/"
              ? pathname === "/" || pathname === "/analysis" || pathname === "/result"
              : pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center justify-center gap-2 rounded-full px-3 py-3 text-xs font-medium transition ${
                isActive
                  ? "bg-[#4CAF50] text-black"
                  : "text-white/55 hover:bg-white/10 hover:text-white"
              }`}
            >
              <Icon className="h-4 w-4" />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}

export default BottomNav;