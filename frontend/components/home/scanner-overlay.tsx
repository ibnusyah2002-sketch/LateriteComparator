const cornerClass =
  "absolute h-10 w-10 border-[#4CAF50] opacity-90";

export function ScannerOverlay() {
  return (
    <div
      className="pointer-events-none absolute inset-5 sm:inset-8"
      aria-hidden="true"
    >
      <span
        className={`${cornerClass} left-0 top-0 border-l-2 border-t-2 rounded-tl-md`}
      />
      <span
        className={`${cornerClass} right-0 top-0 border-r-2 border-t-2 rounded-tr-md`}
      />
      <span
        className={`${cornerClass} bottom-0 left-0 border-b-2 border-l-2 rounded-bl-md`}
      />
      <span
        className={`${cornerClass} bottom-0 right-0 border-b-2 border-r-2 rounded-br-md`}
      />
    </div>
  );
}
