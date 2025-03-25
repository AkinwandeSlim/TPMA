// // theme/theme.ts
// // import { extendTheme } from "@chakra-ui/react"; // Correct import
// // import { extendTheme } from "@chakra-ui/react";
// // import { extendTheme } from '@chakra-ui/react';
// import { extendTheme } from '@chakra-ui/react';
// import { CardComponent } from "./additions/card/card";
// import { buttonStyles } from "./components/button";
// import { badgeStyles } from "./components/badge";
// import { inputStyles } from "./components/input";
// import { progressStyles } from "./components/progress";
// import { sliderStyles } from "./components/slider";
// import { textareaStyles } from "./components/textarea";
// import { switchStyles } from "./components/switch";
// import { linkStyles } from "./components/link";
// import { breakpoints } from "./foundations/breakpoints";
// import { globalStyles } from "./styles";

// export default extendTheme(
//   { breakpoints },
//   globalStyles,
//   badgeStyles,
//   buttonStyles,
//   linkStyles,
//   progressStyles,
//   sliderStyles,
//   inputStyles,
//   textareaStyles,
//   switchStyles,
//   CardComponent
// );




import { extendTheme } from "@chakra-ui/react";
import { CardComponent } from "./additions/card/card";
import { buttonStyles } from "./components/button";
import { badgeStyles } from "./components/badge";
import { inputStyles } from "./components/input";
import { progressStyles } from "./components/progress";
import { sliderStyles } from "./components/slider";
import { textareaStyles } from "./components/textarea";
import { switchStyles } from "./components/switch";
import { linkStyles } from "./components/link";
import { breakpoints } from "./foundations/breakpoints";
import { globalStyles } from "./styles";

export default extendTheme({
  breakpoints, // Spread into a single object
  styles: globalStyles,
  components: {
    Card: CardComponent,
    Button: buttonStyles,
    Badge: badgeStyles,
    Input: inputStyles,
    Progress: progressStyles,
    Slider: sliderStyles,
    Textarea: textareaStyles,
    Switch: switchStyles,
    Link: linkStyles,
  },
});