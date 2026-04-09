import { NavLink } from "react-router-dom";
import { BookOpen, MessageSquare, Mic, FlaskConical } from "lucide-react";
import type { LucideIcon } from "lucide-react";

interface NavItem {
  to: string;
  icon: LucideIcon;
  label: string;
}

const NAV_ITEMS: NavItem[] = [
  { to: "/faqs", icon: BookOpen, label: "FAQs" },
  { to: "/unanswered", icon: MessageSquare, label: "Unanswered" },
  { to: "/voice", icon: Mic, label: "Voice" },
  { to: "/playground", icon: FlaskConical, label: "Playground" },
];

export default function Sidebar() {
  return (
    <aside className="w-56 min-h-screen bg-dark-800 border-r border-dark-600 flex flex-col">
      <div className="p-6 border-b border-dark-600">
        <h1 className="text-gold-400 font-bold text-lg tracking-wide">
          THE MERIDIAN
        </h1>
        <p className="text-gray-500 text-xs mt-1">Concierge Admin</p>
      </div>

      <nav className="flex-1 p-3 space-y-1">
        {NAV_ITEMS.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded text-sm transition-all ${
                isActive
                  ? "bg-gold-500/10 text-gold-400 border border-gold-500/20"
                  : "text-gray-400 hover:text-white hover:bg-dark-600"
              }`
            }
          >
            <Icon size={16} />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}