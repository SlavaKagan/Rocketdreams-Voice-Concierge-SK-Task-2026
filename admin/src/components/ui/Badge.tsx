type BadgeColor = "gold" | "red" | "green" | "gray";

interface BadgeProps {
  children: React.ReactNode;
  color?: BadgeColor;
}

const colorStyles: Record<BadgeColor, string> = {
  gold: "bg-gold-500/10 text-gold-400 border border-gold-500/20",
  red: "bg-red-500/10 text-red-400 border border-red-500/20",
  green: "bg-green-500/10 text-green-400 border border-green-500/20",
  gray: "bg-gray-500/10 text-gray-400 border border-gray-500/20",
};

export default function Badge({ children, color = "gold" }: BadgeProps) {
  return (
    <span
      className={`text-xs px-2 py-0.5 rounded-full font-medium ${colorStyles[color]}`}
    >
      {children}
    </span>
  );
}