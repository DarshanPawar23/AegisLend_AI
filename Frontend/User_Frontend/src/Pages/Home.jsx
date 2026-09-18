import AegisHeader from "../Components/Home_Page/AegisHeader";
import AegisHero from "../Components/Home_Page/AegisHero";
import AegisHLeft from "../Components/Home_Page/Below_Hero/Left/Aegis_H_Left";
import AegisHRight from "../Components/Home_Page/Below_Hero/Right/Aegis_H_Right";
function Home() {
    return (
        <div>
             <AegisHeader  />
             <AegisHero />
             <AegisHLeft />
                <AegisHRight />
        </div>
    );
}
export default Home;
