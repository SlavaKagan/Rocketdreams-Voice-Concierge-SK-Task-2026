import type { ButtonHTMLAttributes } from "react";

type Variant = "primary" | "danger" | "ghost";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
}

const variantStyles: Record<Variant, string> = {
  primary: "bg-gold-500 text-black hover:bg-gold-400",
  danger: "bg-red-600 text-white hover:bg-red-500",
  ghost: "bg-dark-600 text-gray-300 hover:bg-dark-500 border border-dark-500",
};

export default function Button({
  children,
  variant = "primary",
  className = "",
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      disabled={disabled}
      className={`
        px-4 py-2 rounded font-medium transition-all duration-150
        disabled:opacity-50 disabled:cursor-not-allowed
        ${variantStyles[variant]}
        ${className}
      `}
      {...props}
    >
      {children}
    </button>
  );
}