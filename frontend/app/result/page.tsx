import { PageShell } from "@/components/layout/page-shell";
import { BackHeader } from "@/components/layout/back-header";
import { RESULT_DUMMY } from "@/constants/resultDummy";
import { ResultHero } from "@/components/result/result-hero";
import { ImageComparison } from "@/components/result/image-comparison";
import { MaterialSummary } from "@/components/result/material-summary";
import { QaqcGrid } from "@/components/result/qaqc-grid";
import { DescriptionList } from "@/components/result/description-list";
import { AlternativeMatches } from "@/components/result/alternative-matches";
import { ScanAgainAction } from "@/components/result/scan-again-action";
import styles from "@/components/home/home-animations.module.css";

export default function ResultPage() {
  return (
    <PageShell className={styles.fadeIn}>
      <BackHeader title="Comparator Result" backHref="/scan" />

      <main className="flex flex-1 flex-col gap-6 px-4 pb-8">
        <ResultHero result={RESULT_DUMMY} />
        <ImageComparison />
        <MaterialSummary result={RESULT_DUMMY} />
        <QaqcGrid qaqc={RESULT_DUMMY.qaqc} />
        <DescriptionList attributes={RESULT_DUMMY.descriptionAttributes} />
        <AlternativeMatches matches={RESULT_DUMMY.alternativeMatches} />
        <ScanAgainAction />
      </main>
    </PageShell>
  );
}
